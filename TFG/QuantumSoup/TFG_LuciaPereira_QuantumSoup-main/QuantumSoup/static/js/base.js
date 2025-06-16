let lastScrollTop = 0;

window.addEventListener('scroll', function () {
  const header = document.querySelector('header');
  const currentScroll = window.pageYOffset || document.documentElement.scrollTop;

  if (currentScroll > lastScrollTop) {
    // Scroll hacia abajo
    header.classList.add('logo-hidden');
  } else {
    // Scroll hacia arriba
    header.classList.remove('logo-hidden');
  }

  lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
}, false);