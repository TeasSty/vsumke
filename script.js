const products = [
  {
    id: "fringe",
    name: "Замшевая сумка с бахромой",
    price: 4990,
    image: "assets/prod-fringe.jpg",
    alt: "Замшевые сумки с бахромой",
  },
  {
    id: "shoulder",
    name: "Сумка на плечо из замши",
    price: 5490,
    image: "assets/prod-shoulder.jpg",
    alt: "Сумка на плечо из замши",
  },
  {
    id: "olive",
    name: "Сумка Burnt Olive",
    price: 5990,
    image: "assets/prod-olive.jpg",
    alt: "Сумка Burnt Olive",
  },
  {
    id: "compact",
    name: "Компактная сумка",
    price: 4990,
    image: "assets/prod-compact.jpg",
    alt: "Компактная сумка",
  },
];

const formatPrice = (n) =>
  new Intl.NumberFormat("ru-RU").format(n) + " ₽";

const state = {
  cart: JSON.parse(localStorage.getItem("vsumke-cart") || "[]"),
  favs: JSON.parse(localStorage.getItem("vsumke-favs") || "[]"),
};

const els = {
  grid: document.getElementById("products"),
  cartCount: document.getElementById("cartCount"),
  toast: document.getElementById("toast"),
  header: document.getElementById("header"),
  nav: document.getElementById("nav"),
  menuToggle: document.getElementById("menuToggle"),
  year: document.getElementById("year"),
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
  if (els.cartCount) {
    els.cartCount.textContent = String(state.cart.length);
  }
}

function renderProducts() {
  if (!els.grid) return;
  els.grid.innerHTML = products
    .map((p, i) => {
      const liked = state.favs.includes(p.id);
      return `
      <article class="product" style="animation-delay:${i * 0.08}s">
        <div class="product__media">
          <img src="${p.image}" alt="${p.alt}" width="640" height="640" loading="lazy" />
          <button class="fav ${liked ? "is-active" : ""}" type="button" data-fav="${p.id}" aria-label="В избранное" aria-pressed="${liked}">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 20s-7-4.4-7-9.2A4.2 4.2 0 0 1 12 7a4.2 4.2 0 0 1 7 3.8C19 15.6 12 20 12 20z"/></svg>
          </button>
        </div>
        <h3 class="product__name">${p.name}</h3>
        <span class="product__price">${formatPrice(p.price)}</span>
      </article>`;
    })
    .join("");
}

els.grid?.addEventListener("click", (e) => {
  const favBtn = e.target.closest("[data-fav]");
  if (!favBtn) return;

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
  showToast("Каталог ниже на странице");
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

if (els.year) {
  els.year.textContent = String(new Date().getFullYear());
}

renderProducts();
updateBadges();
