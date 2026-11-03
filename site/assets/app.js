(() => {
  'use strict';

  const REPO = 'https://github.com/yunyiforge/rsi-autoresearch-tracker';
  const PAGE_SIZE = 50;
  const TOPIC_LABEL = { rsi: 'RSI', autoresearch: 'AutoResearch' };
  const SOURCE_LABEL = { arxiv: 'arXiv', github: 'GitHub', hn: 'Hacker News', rss: '博客 RSS', curated: '人工精选', auto: '自动发现' };
  const TYPE_LABEL = { paper: '论文', repo: '仓库', article: '博文', discussion: '讨论' };
  const STATUS_LABEL = { curated: '精选', candidate: '候选' };

  const app = document.getElementById('app');
  const cache = {};
  let version = '';

  // ---------- utils ----------
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const safeUrl = (u) => (typeof u === 'string' && /^https?:\/\//i.test(u) ? u : null);
  const link = (u, text, cls = '') => {
    const url = safeUrl(u);
    return url ? `<a href="${esc(url)}" target="_blank" rel="noopener"${cls ? ` class="${cls}"` : ''}>${esc(text)}</a>` : esc(text);
  };
  const day = (s) => (s ? String(s).slice(0, 10) : '');
  const fmt = (n) => (n == null ? '' : Number(n).toLocaleString('en-US'));
  const arr = (v) => (Array.isArray(v) ? v : v == null || v === '' ? [] : [v]);
  const topicLabel = (t) => TOPIC_LABEL[t] || t;
  const hrefFor = (route, params) => {
    const qs = new URLSearchParams(Object.entries(params).filter(([, v]) => v !== '' && v != null)).toString();
    return `#/${route}${qs ? `?${qs}` : ''}`;
  };
  const debounce = (fn, ms) => {
    let t;
    return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); };
  };

  async function fetchText(path, bust = true) {
    const url = bust && version ? `${path}?v=${encodeURIComponent(version)}` : path;
    const res = await fetch(url, { cache: bust ? 'default' : 'no-cache' });
    if (!res.ok) throw new Error(`${path}: HTTP ${res.status}`);
    return res.text();
  }

  function load(name) {
    if (cache[name]) return cache[name];
    const parseJsonl = (t) => t.split('\n').filter((l) => l.trim()).map((l) => JSON.parse(l));
    const spec = {
      stats: ['data/stats.json', JSON.parse, false],
      items: ['data/items.jsonl', parseJsonl],
      frameworks: ['data/frameworks.json', JSON.parse],
      benchmarks: ['data/benchmarks.jsonl', parseJsonl],
      tasks: ['data/benchmark_tasks.jsonl', parseJsonl],
      reportsIndex: ['reports/index.json', JSON.parse, false],
    }[name];
    cache[name] = fetchText(spec[0], spec[2] !== false).then(spec[1]).catch((e) => {
      delete cache[name];
      throw e;
    });
    return cache[name];
  }

  function countBy(rows, get) {
    const m = new Map();
    for (const r of rows) for (const v of arr(get(r))) m.set(v, (m.get(v) || 0) + 1);
    return [...m.entries()].sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0])));
  }

  function bars(entries, hrefFn, labelFn = (k) => k) {
    const max = Math.max(1, ...entries.map((e) => e[1]));
    return `<div class="bars">${entries.map(([k, v]) => `
      <div class="bar">
        ${hrefFn ? `<a href="${esc(hrefFn(k))}" title="${esc(labelFn(k))}">${esc(labelFn(k))}</a>` : `<span class="k">${esc(labelFn(k))}</span>`}
        <div class="track"><div class="fill" style="width:${((v / max) * 100).toFixed(1)}%"></div></div>
        <span class="v">${fmt(v)}</span>
      </div>`).join('')}</div>`;
  }

  // ---------- routing ----------
  function parseHash() {
    const h = location.hash.replace(/^#\/?/, '');
    const [route, qs] = h.split('?');
    return { route: route || '', params: new URLSearchParams(qs || '') };
  }

  const routes = { '': renderOverview, items: renderItems, frameworks: renderFrameworks, benchmarks: renderBenchmarks, tasks: renderTasks, reports: renderReports };

  async function router() {
    const { route, params } = parseHash();
    document.querySelectorAll('#nav a').forEach((a) => a.classList.toggle('active', a.dataset.route === route));
    const fn = routes[route] || renderOverview;
    app.innerHTML = '<p class="muted">加载中…</p>';
    try {
      await fn(params);
    } catch (e) {
      console.error(e);
      app.innerHTML = `<p class="error">加载失败：${esc(e.message)}</p>`;
    }
    window.scrollTo(0, 0);
  }

  // ---------- generic filterable list ----------
  function listPage(opts) {
    const { route, title, lead, rows, filters, sorts, searchText, renderRows, params } = opts;
    const searchIndex = new Map(rows.map((r) => [r, searchText(r).toLowerCase()]));
    const state = Object.fromEntries(params.entries());

    const filterHtml = filters.map((f) => {
      const options = f.options || countBy(rows, f.get).map(([v, c]) => [v, `${f.labelFn ? f.labelFn(v) : v} (${c})`]);
      return `<select data-key="${esc(f.key)}" aria-label="${esc(f.title)}">
        <option value="">${esc(f.title)}：全部</option>
        ${options.map(([v, l]) => `<option value="${esc(v)}">${esc(l)}</option>`).join('')}
      </select>`;
    }).join('');
    app.innerHTML = `
      <h1>${esc(title)}</h1>
      <p class="lead">${lead}</p>
      <div class="toolbar">
        <input type="search" data-key="q" placeholder="搜索标题、摘要、作者、标签…" aria-label="搜索">
        ${filterHtml}
        <select data-key="sort" aria-label="排序">${sorts.map(([k, l]) => `<option value="${esc(k)}">${esc(l)}</option>`).join('')}</select>
        <button type="button" data-reset>重置</button>
      </div>
      <p class="count" id="count"></p>
      <div id="results"></div>
      <div class="pager" id="pager"></div>`;

    const controls = app.querySelectorAll('.toolbar [data-key]');
    controls.forEach((el) => { el.value = state[el.dataset.key] || ''; if (el.tagName === 'SELECT' && !el.value) el.selectedIndex = 0; });

    const update = () => {
      history.replaceState(null, '', hrefFor(route, state));
      draw();
    };
    controls.forEach((el) => {
      const handler = () => { state[el.dataset.key] = el.value; delete state.p; update(); };
      el.addEventListener(el.type === 'search' ? 'input' : 'change', el.type === 'search' ? debounce(handler, 150) : handler);
    });
    app.querySelector('[data-reset]').addEventListener('click', () => {
      Object.keys(state).forEach((k) => delete state[k]);
      controls.forEach((el) => { el.value = ''; if (el.tagName === 'SELECT') el.selectedIndex = 0; });
      update();
    });

    function draw() {
      const terms = (state.q || '').toLowerCase().split(/\s+/).filter(Boolean);
      let out = rows.filter((r) => {
        for (const f of filters) {
          const v = state[f.key];
          if (!v) continue;
          if (f.match ? !f.match(r, v) : !arr(f.get(r)).map(String).includes(v)) return false;
        }
        const text = searchIndex.get(r);
        return terms.every((t) => text.includes(t));
      });
      const sort = sorts.find(([k]) => k === state.sort) || sorts[0];
      out = out.slice().sort(sort[2]);
      const pages = Math.max(1, Math.ceil(out.length / PAGE_SIZE));
      const page = Math.min(pages, Math.max(1, parseInt(state.p, 10) || 1));
      app.querySelector('#count').textContent = `共 ${out.length} 条（总计 ${rows.length}）`;
      app.querySelector('#results').innerHTML = out.length
        ? renderRows(out.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE))
        : '<p class="muted">没有匹配的结果。</p>';
      const pager = app.querySelector('#pager');
      pager.innerHTML = pages > 1
        ? `<button type="button" data-p="${page - 1}" ${page <= 1 ? 'disabled' : ''}>上一页</button>
           <span class="muted">第 ${page} / ${pages} 页</span>
           <button type="button" data-p="${page + 1}" ${page >= pages ? 'disabled' : ''}>下一页</button>`
        : '';
      pager.querySelectorAll('button[data-p]').forEach((b) => b.addEventListener('click', () => {
        state.p = b.dataset.p;
        update();
        app.querySelector('#count').scrollIntoView({ block: 'start' });
      }));
      app.querySelectorAll('.summary.clamp').forEach((s) => s.addEventListener('click', () => s.classList.remove('clamp')));
    }
    draw();
  }

  const desc = (get) => (a, b) => (get(b) ?? -Infinity) > (get(a) ?? -Infinity) ? 1 : (get(b) ?? -Infinity) < (get(a) ?? -Infinity) ? -1 : 0;
  const asc = (get) => (a, b) => String(get(a) ?? '').localeCompare(String(get(b) ?? ''));

  function topicChips(topics, route) {
    return arr(topics).map((t) => `<a class="chip topic" href="${esc(hrefFor(route, { topic: t }))}">${esc(topicLabel(t))}</a>`).join('');
  }
  function tagChips(tags, route) {
    return arr(tags).map((t) => `<a class="chip" href="${esc(hrefFor(route, { tag: t }))}">#${esc(t)}</a>`).join('');
  }
  const statusBadge = (s) => `<span class="badge ${esc(s)}">${esc(STATUS_LABEL[s] || s)}</span>`;

  // ---------- overview ----------
  async function renderOverview() {
    const s = await load('stats');
    const c = s.counts || {};
    const fw = s.frameworks || {};
    const bm = s.benchmarks || {};
    app.innerHTML = `
      <h1>RSI &amp; AutoResearch 每日追踪</h1>
      <p class="lead">每天自动采集 <b>递归自我改进（RSI）</b> 与 <b>AI 自动科研（AutoResearch）</b> 相关的论文、开源仓库、社区讨论和博客，并构建技术框架清单、Benchmark 目录与论文复现任务候选集。最近一次运行：${esc(s.run_date || '')}（${esc(s.generated_at || '')}）。</p>
      <div class="stats">
        <a class="stat" href="#/items"><div class="num">${fmt(c.items_total)}</div><div class="label">条目总数</div></a>
        <a class="stat" href="#/items?new=1"><div class="num">${fmt(c.new_today)}</div><div class="label">今日新增条目</div></a>
        <a class="stat" href="#/frameworks"><div class="num">${fmt(fw.total)}</div><div class="label">技术框架（精选 ${fmt(fw.curated)}）</div></a>
        <a class="stat" href="#/benchmarks"><div class="num">${fmt(bm.total)}</div><div class="label">Benchmark（精选 ${fmt(bm.curated)}）</div></a>
        <a class="stat" href="#/tasks"><div class="num">${fmt(s.benchmark_tasks)}</div><div class="label">论文复现任务候选</div></a>
      </div>
      <div class="grid2">
        <div class="panel"><h2>按数据源</h2>${bars(Object.entries(c.by_source || {}), (k) => hrefFor('items', { source: k }), (k) => SOURCE_LABEL[k] || k)}
          <h2>按主题</h2>${bars(Object.entries(c.by_topic || {}), (k) => hrefFor('items', { topic: k }), topicLabel)}</div>
        <div class="panel"><h2>按标签</h2>${bars(Object.entries(c.by_tag || {}), (k) => hrefFor('items', { tag: k }))}</div>
        <div class="panel"><h2>框架类别</h2>${bars(Object.entries(fw.by_category || {}), (k) => hrefFor('frameworks', { category: k }))}</div>
        <div class="panel"><h2>Benchmark 方向</h2>${bars(Object.entries(bm.by_focus || {}), (k) => hrefFor('benchmarks', { focus: k }))}</div>
      </div>
      <div class="grid2">
        <div class="panel"><h2>最新高相关条目</h2><div id="latest" class="muted">加载中…</div></div>
        <div class="panel"><h2>Star 最多的框架</h2><div id="topfw" class="muted">加载中…</div></div>
      </div>
      <h2>数据源健康</h2>
      <div class="table-wrap"><table>
        <thead><tr><th>数据源</th><th>状态</th><th class="num">抓取</th><th class="num">耗时 (s)</th><th>错误</th></tr></thead>
        <tbody>${Object.entries(s.sources || {}).map(([k, v]) => `
          <tr><td>${esc(SOURCE_LABEL[k] || k)}</td>
          <td class="${v.status === 'ok' ? 'status-ok' : 'status-bad'}">${esc(v.status)}</td>
          <td class="num">${fmt(v.fetched)}</td><td class="num">${esc(v.seconds ?? '')}</td>
          <td class="small">${esc(arr(v.errors).join('; '))}</td></tr>`).join('')}</tbody>
      </table></div>
      <p class="small muted">流水线：采集 ${fmt(s.pipeline?.collected)} 条，过滤不相关 ${fmt(s.pipeline?.irrelevant_filtered)} 条，去重 ${fmt(s.pipeline?.duplicates_removed)} 条，跨源关联 ${fmt(s.pipeline?.cross_links)} 处；质量检查：${s.quality?.passed ? '<span class="status-ok">通过</span>' : '<span class="status-bad">未通过</span>'}。</p>`;

    const [items, frameworks] = await Promise.all([load('items'), load('frameworks')]);
    const latest = items.filter((i) => (i.relevance || 0) >= 4).sort(desc((i) => i.published || '')).slice(0, 10);
    const el = app.querySelector('#latest');
    if (el) el.outerHTML = `<div class="list">${latest.map((i) => `
      <div><div>${link(i.url, i.title)}</div>
      <div class="small muted">${esc(SOURCE_LABEL[i.source] || i.source)} · ${esc(day(i.published))} · 相关度 ${esc(i.relevance)}</div></div>`).join('')}
      <a href="#/items?sort=published">查看全部 →</a></div>`;
    const top = frameworks.slice().sort(desc((f) => f.stars)).slice(0, 10);
    const el2 = app.querySelector('#topfw');
    if (el2) el2.outerHTML = bars(top.map((f) => [f.name, f.stars || 0]), (k) => hrefFor('frameworks', { q: k }));
  }

  // ---------- items ----------
  async function renderItems(params) {
    const [items, stats] = await Promise.all([load('items'), load('stats')]);
    const runDate = stats.run_date;
    listPage({
      route: 'items',
      title: '条目库',
      lead: '论文、开源仓库、Hacker News 讨论与博客文章，已去重、分类和打标签。点击标签可快速筛选。',
      rows: items,
      params,
      filters: [
        { key: 'source', title: '来源', get: (i) => i.source, labelFn: (v) => SOURCE_LABEL[v] || v },
        { key: 'type', title: '类型', get: (i) => i.type, labelFn: (v) => TYPE_LABEL[v] || v },
        { key: 'topic', title: '主题', get: (i) => i.topics, labelFn: topicLabel },
        { key: 'tag', title: '标签', get: (i) => i.tags },
        { key: 'rel', title: '相关度', options: [3, 4, 5, 6].map((n) => [String(n), `≥ ${n}`]), match: (i, v) => (i.relevance || 0) >= Number(v) },
        { key: 'new', title: '时间', options: [['1', `今日新增（${runDate}）`]], match: (i) => day(i.first_seen) === runDate },
      ],
      sorts: [
        ['published', '最新发布', desc((i) => i.published || '')],
        ['relevance', '相关度', (a, b) => (b.relevance || 0) - (a.relevance || 0) || desc((i) => i.published || '')(a, b)],
        ['stars', 'Star / 热度', desc((i) => i.metrics?.stars ?? i.metrics?.points ?? -1)],
        ['first_seen', '最近收录', desc((i) => i.first_seen || '')],
      ],
      searchText: (i) => [i.title, i.summary, arr(i.authors).join(' '), arr(i.tags).join(' '), arr(i.topics).join(' '), i.id].join(' '),
      renderRows: (rows) => `<div class="list">${rows.map(itemCard).join('')}</div>`,
    });
  }

  function itemCard(i) {
    const m = i.metrics || {};
    const authors = arr(i.authors);
    const metaParts = [
      `<span>${esc(SOURCE_LABEL[i.source] || i.source)} · ${esc(TYPE_LABEL[i.type] || i.type)}</span>`,
      i.published ? `<span>${esc(day(i.published))}</span>` : '',
      authors.length ? `<span>${esc(authors.slice(0, 3).join(', '))}${authors.length > 3 ? ' 等' : ''}</span>` : '',
      i.extra?.feed ? `<span>${esc(i.extra.feed)}</span>` : '',
      m.stars != null ? `<span>★ ${fmt(m.stars)}</span>` : '',
      m.points != null ? `<span>▲ ${fmt(m.points)} · 💬 ${fmt(m.comments)}</span>` : '',
      i.extra?.language ? `<span>${esc(i.extra.language)}</span>` : '',
      `<span>相关度 ${esc(i.relevance)}</span>`,
      i.links?.pdf ? `<span>${link(i.links.pdf, 'PDF')}</span>` : '',
      i.links?.discussion ? `<span>${link(i.links.discussion, '讨论')}</span>` : '',
      ...arr(i.extra?.code_repos).map((u) => `<span>${link(u, '💻 代码')}</span>`),
    ];
    const summary = String(i.summary || '').trim();
    return `<div class="card">
      <div class="title">${link(i.url, i.title)}</div>
      <div class="meta">${metaParts.join('')}</div>
      ${summary ? `<div class="summary clamp" title="点击展开">${esc(summary)}</div>` : ''}
      <div class="chips">${topicChips(i.topics, 'items')}${tagChips(i.tags, 'items')}</div>
    </div>`;
  }

  // ---------- frameworks ----------
  async function renderFrameworks(params) {
    const rows = await load('frameworks');
    listPage({
      route: 'frameworks',
      title: '技术框架清单',
      lead: `人工精选 + 自动发现的 RSI / AutoResearch 技术框架。数据：${link(`${REPO}/blob/main/data/frameworks.json`, 'JSON')} · ${link(`${REPO}/blob/main/data/frameworks.csv`, 'CSV')}`,
      rows,
      params,
      filters: [
        { key: 'category', title: '类别', get: (f) => f.category },
        { key: 'status', title: '状态', get: (f) => f.status, labelFn: (v) => STATUS_LABEL[v] || v },
        { key: 'topic', title: '主题', get: (f) => f.topics, labelFn: topicLabel },
        { key: 'language', title: '语言', get: (f) => f.language },
      ],
      sorts: [
        ['stars', 'Star 数', desc((f) => f.stars ?? -1)],
        ['last_push', '最近更新', desc((f) => f.last_push || '')],
        ['year', '年份', desc((f) => f.year ?? 0)],
        ['name', '名称', asc((f) => f.name.toLowerCase())],
      ],
      searchText: (f) => [f.name, f.org, f.repo, f.description, f.category, arr(f.topics).join(' ')].join(' '),
      renderRows: (list) => `<div class="table-wrap"><table>
        <thead><tr><th>名称</th><th>类别</th><th>状态</th><th class="hide-sm">机构 / 作者</th><th>主题</th><th class="num">★</th><th class="hide-sm">语言</th><th class="hide-sm">最近推送</th><th>论文</th></tr></thead>
        <tbody>${list.map((f) => `<tr>
          <td>${link(f.url || (f.repo ? `https://github.com/${f.repo}` : null), f.name)}<div class="desc">${esc(f.description)}</div></td>
          <td>${esc(f.category)}</td>
          <td>${statusBadge(f.status)}</td>
          <td class="hide-sm">${esc(f.org || '')}</td>
          <td><div class="chips" style="margin:0">${topicChips(f.topics, 'frameworks')}</div></td>
          <td class="num">${fmt(f.stars)}</td>
          <td class="hide-sm">${esc(f.language || '')}</td>
          <td class="hide-sm nowrap">${esc(day(f.last_push))}</td>
          <td>${f.arxiv_id ? link(`https://arxiv.org/abs/${f.arxiv_id}`, f.arxiv_id) : ''}</td>
        </tr>`).join('')}</tbody></table></div>`,
    });
  }

  // ---------- benchmarks ----------
  async function renderBenchmarks(params) {
    const rows = await load('benchmarks');
    listPage({
      route: 'benchmarks',
      title: 'Benchmark 目录',
      lead: `评测 AI 自动科研 / 自我改进能力的 benchmark（人工精选 + 自动发现）。数据：${link(`${REPO}/blob/main/data/benchmarks.jsonl`, 'JSONL')} · ${link(`${REPO}/blob/main/data/benchmarks.csv`, 'CSV')}`,
      rows,
      params,
      filters: [
        { key: 'focus', title: '方向', get: (b) => b.focus },
        { key: 'status', title: '状态', get: (b) => b.status, labelFn: (v) => STATUS_LABEL[v] || v },
        { key: 'topic', title: '主题', get: (b) => b.topics, labelFn: topicLabel },
      ],
      sorts: [
        ['status', '精选优先', (a, b) => (a.status === 'curated' ? 0 : 1) - (b.status === 'curated' ? 0 : 1) || (b.year || 0) - (a.year || 0)],
        ['year', '年份', desc((b) => b.year ?? 0)],
        ['stars', 'Star 数', desc((b) => b.stars ?? -1)],
        ['name', '名称', asc((b) => b.name.toLowerCase())],
      ],
      searchText: (b) => [b.name, b.org, b.description, b.focus, b.metric, b.tasks, b.arxiv_id, arr(b.topics).join(' ')].join(' '),
      renderRows: (list) => `<div class="table-wrap"><table>
        <thead><tr><th>名称</th><th>方向</th><th>状态</th><th class="hide-sm">机构</th><th>年份</th><th class="hide-sm">任务 / 指标</th><th class="num">★</th><th>链接</th></tr></thead>
        <tbody>${list.map((b) => `<tr>
          <td>${link(b.homepage || b.paper_url || (b.repo ? `https://github.com/${b.repo}` : null), b.name)}<div class="desc">${esc(b.description)}</div>
            <div class="chips">${topicChips(b.topics, 'benchmarks')}</div></td>
          <td>${esc(b.focus)}</td>
          <td>${statusBadge(b.status)}</td>
          <td class="hide-sm">${esc(b.org || '')}</td>
          <td>${esc(b.year || '')}</td>
          <td class="hide-sm small">${b.tasks ? `<div>📋 ${esc(b.tasks)}</div>` : ''}${b.metric ? `<div>📏 ${esc(b.metric)}</div>` : ''}</td>
          <td class="num">${fmt(b.stars)}</td>
          <td class="small">${[b.paper_url && link(b.paper_url, '论文'), b.repo && link(`https://github.com/${b.repo}`, '代码'), b.homepage && link(b.homepage, '主页')].filter(Boolean).join(' · ')}</td>
        </tr>`).join('')}</tbody></table></div>`,
    });
  }

  // ---------- tasks ----------
  async function renderTasks(params) {
    const rows = await load('tasks');
    listPage({
      route: 'tasks',
      title: '论文复现任务候选',
      lead: `PaperBench 风格：从「相关论文 + 官方代码」自动生成的复现任务，官方仓库作为评分参考。数据：${link(`${REPO}/blob/main/data/benchmark_tasks.jsonl`, 'JSONL')} · ${link(`${REPO}/blob/main/docs/BENCHMARK_PIPELINE.md`, '构建方法')}`,
      rows,
      params,
      filters: [
        { key: 'difficulty', title: '难度', get: (t) => t.difficulty_hint },
        { key: 'topic', title: '主题', get: (t) => t.topics, labelFn: topicLabel },
        { key: 'tag', title: '标签', get: (t) => t.tags },
        { key: 'status', title: '状态', get: (t) => t.status },
      ],
      sorts: [
        ['published', '论文发布时间', desc((t) => t.paper?.published || '')],
        ['first_seen', '最近收录', desc((t) => t.first_seen || '')],
        ['title', '标题', asc((t) => t.paper?.title || '')],
      ],
      searchText: (t) => [t.paper?.title, t.paper?.arxiv_id, t.task_id, t.instructions, arr(t.tags).join(' '), arr(t.code_repos).join(' ')].join(' '),
      renderRows: (list) => `<div class="list">${list.map((t) => `<div class="card">
        <div class="title">${link(t.paper?.url, t.paper?.title || t.task_id)}</div>
        <div class="meta">
          <span><code>${esc(t.task_id)}</code></span>
          <span class="badge ${esc(t.difficulty_hint)}">${esc(t.difficulty_hint)}</span>
          <span>${esc(day(t.paper?.published))}</span>
          <span>评分：${esc(t.grading?.type || '')}${t.grading?.reference ? ` · 参考 ${esc(t.grading.reference)}` : ''}${t.grading?.status ? ` · ${esc(t.grading.status)}` : ''}</span>
          ${arr(t.code_repos).map((u) => `<span>${link(u, '💻 官方代码')}</span>`).join('')}
        </div>
        <div class="summary clamp" title="点击展开">${esc(t.instructions)}</div>
        <div class="chips">${topicChips(t.topics, 'tasks')}${tagChips(t.tags, 'tasks')}</div>
      </div>`).join('')}</div>`,
    });
  }

  // ---------- reports (minimal Markdown renderer for the generated reports) ----------
  const unescapeMd = (t) => t.replace(/\\([\\`*_[\]()|#>!-])/g, '$1');
  function resolveHref(href, base) {
    try {
      const u = new URL(href, base);
      return /^https?:$/.test(u.protocol) ? u.href : null;
    } catch { return null; }
  }
  function mdInline(raw, base) {
    const re = /`([^`]+)`|\[((?:\\.|[^\]\\])+)\]\(([^)\s]+)\)|\*\*(.+?)\*\*/g;
    let out = '';
    let last = 0;
    let m;
    while ((m = re.exec(raw))) {
      out += esc(unescapeMd(raw.slice(last, m.index)));
      if (m[1] != null) out += `<code>${esc(m[1])}</code>`;
      else if (m[2] != null) {
        const href = resolveHref(m[3], base);
        const text = mdInline(m[2], base);
        out += href ? `<a href="${esc(href)}" target="_blank" rel="noopener">${text}</a>` : text;
      } else out += `<strong>${mdInline(m[4], base)}</strong>`;
      last = re.lastIndex;
    }
    return out + esc(unescapeMd(raw.slice(last)));
  }
  function renderMarkdown(text, base) {
    const lines = text.replace(/\r/g, '').split('\n');
    const html = [];
    const cells = (l) => l.trim().replace(/^\|/, '').replace(/(?<!\\)\|$/, '').split(/(?<!\\)\|/).map((c) => c.trim());
    let i = 0;
    while (i < lines.length) {
      const line = lines[i];
      let m;
      if (!line.trim()) { i++; continue; }
      if ((m = line.match(/^(#{1,6})\s+(.*)$/))) {
        html.push(`<h${m[1].length}>${mdInline(m[2], base)}</h${m[1].length}>`); i++;
      } else if (/^\s*(-{3,}|\*{3,})\s*$/.test(line)) {
        html.push('<hr>'); i++;
      } else if (/^>/.test(line)) {
        const buf = [];
        while (i < lines.length && /^>/.test(lines[i])) buf.push(lines[i++].replace(/^>\s?/, ''));
        html.push(`<blockquote><p>${mdInline(buf.join(' '), base)}</p></blockquote>`);
      } else if (/^\s*\|/.test(line)) {
        const rows = [];
        while (i < lines.length && /^\s*\|/.test(lines[i])) rows.push(lines[i++]);
        const head = cells(rows[0]);
        const hasSep = rows[1] && /^[\s|:-]+$/.test(rows[1]);
        const align = hasSep ? cells(rows[1]).map((c) => (/^:-+:$/.test(c) ? 'center' : /-:$/.test(c) ? 'right' : '')) : [];
        const td = (tag, c, k) => `<${tag}${align[k] ? ` style="text-align:${align[k]}"` : ''}>${mdInline(c, base)}</${tag}>`;
        html.push(`<table><thead><tr>${head.map((c, k) => td('th', c, k)).join('')}</tr></thead><tbody>${
          rows.slice(hasSep ? 2 : 1).map((r) => `<tr>${cells(r).map((c, k) => td('td', c, k)).join('')}</tr>`).join('')}</tbody></table>`);
      } else if (/^\s*([-*+]|\d+\.)\s+/.test(line)) {
        const ordered = /^\s*\d+\./.test(line);
        const items = [];
        while (i < lines.length && /^\s*([-*+]|\d+\.)\s+/.test(lines[i])) items.push(lines[i++].replace(/^\s*([-*+]|\d+\.)\s+/, ''));
        const tag = ordered ? 'ol' : 'ul';
        html.push(`<${tag}>${items.map((it) => `<li>${mdInline(it, base)}</li>`).join('')}</${tag}>`);
      } else {
        const buf = [];
        while (i < lines.length && lines[i].trim() && !/^(#{1,6}\s|>|\s*\||\s*([-*+]|\d+\.)\s)/.test(lines[i])) buf.push(lines[i++].trim());
        html.push(`<p>${mdInline(buf.join(' '), base)}</p>`);
      }
    }
    return html.join('\n');
  }

  async function renderReports(params) {
    let daily = [];
    try { daily = (await load('reportsIndex')).daily || []; } catch (e) { console.warn(e); }
    const choices = [
      ['LATEST', '今日日报（LATEST）', 'reports/LATEST.md'],
      ['FRAMEWORKS', '技术框架报告', 'reports/FRAMEWORKS.md'],
      ['BENCHMARKS', 'Benchmark 报告', 'reports/BENCHMARKS.md'],
      ...daily.map((d) => [d, `日报 ${d}`, `reports/daily/${d}.md`]),
    ];
    const current = choices.find(([k]) => k === params.get('r')) || choices[0];
    app.innerHTML = `
      <h1>报告</h1>
      <p class="lead">由流水线自动生成的 Markdown 报告。${link(`${REPO}/tree/main/reports`, '在 GitHub 查看全部')}</p>
      <div class="toolbar"><label>选择报告 <select id="report">${choices.map(([k, l]) => `<option value="${esc(k)}"${k === current[0] ? ' selected' : ''}>${esc(l)}</option>`).join('')}</select></label></div>
      <div id="md" class="markdown"><p class="muted">加载中…</p></div>`;
    app.querySelector('#report').addEventListener('change', (e) => { location.hash = hrefFor('reports', { r: e.target.value }); });

    const text = await fetchText(current[2]);
    app.querySelector('#md').innerHTML = renderMarkdown(text, `${REPO}/blob/main/${current[2]}`);
  }

  // ---------- boot ----------
  async function boot() {
    try {
      const s = await load('stats');
      version = s.generated_at || '';
      document.getElementById('updated').textContent = `数据更新于 ${s.generated_at || '未知'}（UTC）`;
    } catch (e) {
      console.warn(e);
    }
    window.addEventListener('hashchange', router);
    router();
  }
  boot();
})();
