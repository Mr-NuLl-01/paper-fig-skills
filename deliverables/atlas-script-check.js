
"use strict";
(() => {
  const papers = Array.from(document.querySelectorAll("article.paper"));
  const search = document.getElementById("search");
  const category = document.getElementById("category");
  const tier = document.getElementById("tier");
  const status = document.getElementById("result-count");
  const empty = document.getElementById("empty");
  const normalize = value => value.toLocaleLowerCase().normalize("NFKC");
  function applyFilters() {
    const terms = normalize(search.value).trim().split(/\s+/u).filter(Boolean);
    let count = 0;
    for (const paper of papers) {
      const match = (!category.value || paper.dataset.category === category.value)
        && (!tier.value || paper.dataset.tier === tier.value)
        && terms.every(term => normalize(paper.dataset.search).includes(term));
      paper.hidden = !match;
      if (match) count += 1;
    }
    status.textContent = `显示 ${count} / ${papers.length} 篇`;
    empty.hidden = count !== 0;
  }
  search.addEventListener("input", applyFilters);
  category.addEventListener("change", applyFilters);
  tier.addEventListener("change", applyFilters);
  document.getElementById("reset").addEventListener("click", () => {
    search.value = ""; category.value = ""; tier.value = ""; applyFilters(); search.focus();
  });
  document.getElementById("expand").addEventListener("click", () => {
    papers.filter(p => !p.hidden).forEach(p => {p.querySelector(".paper-details").open = true;});
  });
  document.getElementById("collapse").addEventListener("click", () => {
    papers.filter(p => !p.hidden).forEach(p => {p.querySelector(".paper-details").open = false;});
  });
  function openHash() {
    const id = decodeURIComponent(location.hash.slice(1));
    const paper = papers.find(p => p.id === id);
    if (!paper) return;
    search.value = ""; category.value = ""; tier.value = ""; applyFilters();
    paper.querySelector(".paper-details").open = true;
    requestAnimationFrame(() => paper.scrollIntoView({block: "start"}));
  }
  window.addEventListener("hashchange", openHash);
  applyFilters(); openHash();
})();
