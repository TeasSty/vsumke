const products = [
  {
    id: "fringe",
    name: "Замшевая сумка с бахромой",
    price: 4990,
    image: "assets/bag1.jpg",
    alt: "Две замшевые сумки с бахромой",
    position: "center 42%",
    category: "Сумки",
    hit: true,
  },
  {
    id: "shoulder",
    name: "Сумка на плечо из замши",
    price: 5490,
    image: "assets/vk-08.jpg",
    alt: "Тёмно-коричневая замшевая сумка на плечо",
    position: "center 60%",
    category: "Сумки",
  },
  {
    id: "olive",
    name: "Сумка Burnt Olive",
    price: 5990,
    image: "assets/bag3.jpg",
    alt: "Замшевая сумка цвета burnt olive",
    position: "center",
    zoom: 2.85,
    origin: "12% 60%",
    category: "Сумки",
  },
  {
    id: "shopper",
    name: "Сумка-шопер",
    price: 5490,
    image: "assets/vk-14.jpg",
    alt: "Вместительная сумка-шопер",
    position: "center 48%",
    category: "Шопперы",
  },
  {
    id: "classic",
    name: "Классическая сумка",
    price: 5990,
    image: "assets/vk-12.jpg",
    alt: "Классическая замшевая сумка",
    position: "center 42%",
    category: "Сумки",
  },
  {
    id: "everyday",
    name: "Сумка в повседневном стиле",
    price: 5490,
    image: "assets/vk-06.jpg",
    alt: "Повседневная замшевая сумка на плече",
    position: "center 48%",
    category: "Сумки",
  },
  {
    id: "chain",
    name: "Сумка с цепочкой",
    price: 4990,
    image: "assets/vk-16.jpg",
    alt: "Оливковая сумка с цепочкой",
    position: "center 62%",
    category: "Кросс-боды",
    also: "Аксессуары",
  },
  {
    id: "shoulder-green",
    name: "Сумка на плечо",
    price: 5490,
    image: "assets/vk-17.jpg",
    alt: "Зелёная сумка на плечо",
    position: "center 58%",
    category: "Сумки",
  },
];

const formatPrice = (n) => new Intl.NumberFormat("ru-RU").format(n) + " ₽";

const state = {
  cart: JSON.parse(localStorage.getItem("vsumke-cart") || "[]"),
  favs: JSON.parse(localStorage.getItem("vsumke-favs") || "[]"),
  filter: "all",
};

const els = {
  grid: document.getElementById("products"),
  cartCount: document.getElementById("cartCount"),
  toast: document.getElementById("toast"),
  header: document.getElementById("header"),
  nav: document.getElementById("nav"),
  menuToggle: document.getElementById("menuToggle"),
  year: document.getElementById("year"),
  chips: document.getElementById("chips"),
  empty: document.getElementById("catalogEmpty"),
};

function persist() {
  localStorage.setItem("vsumke-cart", JSON.stringify(state.cart));
  localStorage.setItem("vsumke-favs", JSON.stringify(state.favs));
}

function showToast(message) {
  if (!els.toast) return;
  els.toast.hidden = false;
  els.toast.textContent = message;
  els.toast.classList.add("is-visible");
  clearTimeout(showToast._t);
  showToast._t = setTimeout(() => {
    els.toast.classList.remove("is-visible");
  }, 2200);
}

function updateBadges() {
  if (!els.cartCount) return;
  const n = state.cart.length;
  els.cartCount.textContent = String(n);
  els.cartCount.hidden = n === 0;
}

function renderProducts() {
  if (!els.grid) return;
  els.grid.innerHTML = products
    .map((p) => {
      const liked = state.favs.includes(p.id);
      const hit = p.hit
        ? `<span class="product__hit">Хит</span>`
        : "";
      const cats = [p.category, p.also].filter(Boolean).join("|");
      const zoom = p.zoom ? `--zoom:${p.zoom};--origin:${p.origin};` : "";
      return `
      <article class="product" data-cats="${cats}">
        <div class="product__media">
          ${hit}
          <img src="${p.image}" alt="${p.alt}" width="640" height="640" loading="lazy" style="object-position:${p.position};${zoom}" />
          <button class="fav ${liked ? "is-active" : ""}" type="button" data-fav="${p.id}" aria-label="В избранное" aria-pressed="${liked}">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M12 20s-7-4.4-7-9.2A4.2 4.2 0 0 1 12 7a4.2 4.2 0 0 1 7 3.8C19 15.6 12 20 12 20z"/></svg>
          </button>
        </div>
        <h3 class="product__name">${p.name}</h3>
        <span class="product__price">${formatPrice(p.price)}</span>
        <button class="product__cart" type="button" data-add="${p.id}">В корзину</button>
      </article>`;
    })
    .join("");
  applyFilter(state.filter);
}

function applyFilter(cat) {
  state.filter = cat;
  let shown = 0;
  els.grid?.querySelectorAll(".product").forEach((el) => {
    const match = cat === "all" || (el.dataset.cats || "").split("|").includes(cat);
    el.hidden = !match;
    if (match) shown += 1;
  });
  if (els.empty) els.empty.hidden = shown !== 0;
  els.chips?.querySelectorAll(".chip").forEach((btn) => {
    const on = btn.dataset.filter === cat;
    btn.classList.toggle("is-active", on);
    btn.setAttribute("aria-pressed", String(on));
  });
}

els.grid?.addEventListener("click", (e) => {
  const favBtn = e.target.closest("[data-fav]");
  if (favBtn) {
    const id = favBtn.dataset.fav;
    if (state.favs.includes(id)) {
      state.favs = state.favs.filter((x) => x !== id);
      showToast("Убрано из избранного");
    } else {
      state.favs.push(id);
      showToast("Добавлено в избранное");
    }
    persist();
    renderProducts();
    return;
  }

  const addBtn = e.target.closest("[data-add]");
  if (!addBtn) return;
  state.cart.push(addBtn.dataset.add);
  persist();
  updateBadges();
  showToast("Добавлено в корзину");
});

els.chips?.addEventListener("click", (e) => {
  const btn = e.target.closest("[data-filter]");
  if (!btn) return;
  applyFilter(btn.dataset.filter);
});

document.getElementById("cartBtn")?.addEventListener("click", () => {
  if (!state.cart.length) {
    showToast("Корзина пока пуста");
    return;
  }
  showToast(`В корзине: ${state.cart.length}. Оформление — через ВК`);
});

document.getElementById("favBtn")?.addEventListener("click", () => {
  showToast(
    state.favs.length
      ? `В избранном: ${state.favs.length}`
      : "Избранное пока пусто"
  );
});

document.getElementById("searchBtn")?.addEventListener("click", () => {
  document.getElementById("catalog")?.scrollIntoView({ behavior: "smooth" });
});

els.menuToggle?.addEventListener("click", () => {
  const open = els.nav.classList.toggle("is-open");
  els.menuToggle.setAttribute("aria-expanded", String(open));
});

els.nav?.querySelectorAll("a").forEach((a) => {
  a.addEventListener("click", () => {
    els.nav.classList.remove("is-open");
    els.menuToggle?.setAttribute("aria-expanded", "false");
  });
});

window.addEventListener(
  "scroll",
  () => {
    els.header?.classList.toggle("is-scrolled", window.scrollY > 8);
  },
  { passive: true }
);

if (els.year) els.year.textContent = String(new Date().getFullYear());

renderProducts();
updateBadges();
