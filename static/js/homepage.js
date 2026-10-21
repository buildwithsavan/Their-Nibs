

document.addEventListener('DOMContentLoaded', () => {

  const header = document.querySelector('.site-header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      header?.classList.add('scrolled');
    } else {
      header?.classList.remove('scrolled');
    }
  });
  
  const announceItems = document.querySelectorAll('.announcement-item');
  const prevAnnounce = document.getElementById('prevAnnounce');
  const nextAnnounce = document.getElementById('nextAnnounce');
  let currentAnnounce = 0;

  function showAnnounce(idx) {
    if (!announceItems.length) return;
    announceItems.forEach((el, i) => {
      el.classList.toggle('active', i === idx);
    });
    currentAnnounce = idx;
  }

  if (prevAnnounce && nextAnnounce && announceItems.length > 1) {
    prevAnnounce.addEventListener('click', () => {
      const prev = (currentAnnounce - 1 + announceItems.length) % announceItems.length;
      showAnnounce(prev);
    });

    nextAnnounce.addEventListener('click', () => {
      const next = (currentAnnounce + 1) % announceItems.length;
      showAnnounce(next);
    });

    setInterval(() => {
      const next = (currentAnnounce + 1) % announceItems.length;
      showAnnounce(next);
    }, 5000);
  }

  const navItems = document.querySelectorAll('.nav-desktop .nav-item');
  const navLinks = document.querySelectorAll('.nav-desktop .nav-link');

  navLinks.forEach(link => {
    link.addEventListener('click', function () {
      navItems.forEach(item => item.classList.remove('active'));
      navLinks.forEach(l => l.classList.remove('active'));

      this.classList.add('active');
      const parent = this.closest('.nav-item');
      if (parent) {
        parent.classList.add('active');
      }
    });
  });

  const megaItem = document.querySelector('.nav-item.has-mega-menu');
  const megaMenu = document.querySelector('.women-mega-menu');

  if (megaItem && megaMenu) {
    let megaCloseTimer = null;

    function openMega() {
      clearTimeout(megaCloseTimer);
      megaItem.classList.add('is-open');
      megaMenu.style.opacity = '1';
      megaMenu.style.visibility = 'visible';
      megaMenu.style.pointerEvents = 'auto';
      megaMenu.style.transform = 'translateX(-50%) translateY(0)';
    }

    function scheduleCloseMega() {
      clearTimeout(megaCloseTimer);
      megaCloseTimer = setTimeout(() => {
        megaItem.classList.remove('is-open');
        megaMenu.style.opacity = '';
        megaMenu.style.visibility = '';
        megaMenu.style.pointerEvents = '';
        megaMenu.style.transform = '';
      }, 250);
    }

    megaItem.addEventListener('mouseenter', openMega);
    megaItem.addEventListener('mouseleave', scheduleCloseMega);
    megaMenu.addEventListener('mouseenter', openMega);
    megaMenu.addEventListener('mouseleave', scheduleCloseMega);

    const menuLinks = megaMenu.querySelectorAll('a');
    menuLinks.forEach(a => {
      a.addEventListener('click', function(e) {
        e.stopPropagation();
      });
    });
  }

  
  const heroSubtitle = document.querySelector('.hero-subtitle');
  const heroTitle = document.querySelector('.hero-title');
  const heroBtn = document.querySelector('.hero-btn');
  const heroDots = document.querySelectorAll('.hero-dot');
  const heroPrev = document.querySelector('.hero-prev');
  const heroNext = document.querySelector('.hero-next');

  const slides = [
    {
      subtitle: 'Sophie Ellis-Bextor Collaboration',
      title: 'Sleepwear with star quality',
      btnText: 'SHOP NOW',
      link: '#shop'
    },
    {
      subtitle: 'Autumn Boutique Collection',
      title: 'Elegance woven into every thread',
      btnText: 'EXPLORE WOMENS',
      link: '#womens'
    },
    {
      subtitle: 'Matching Family Lounge Sets',
      title: 'Unmatched comfort for cozy family evenings',
      btnText: 'DISCOVER FAMILY SETS',
      link: '#matching'
    }
  ];

  let currentHeroSlide = 0;
  let heroTimer = null;

  function updateHeroSlide(index) {
    if (!slides[index]) return;
    currentHeroSlide = index;
    
    const heroContent = document.querySelector('.hero-content');
    if (heroContent) {
      heroContent.style.opacity = '0';
      heroContent.style.transform = 'translateY(6px)';
      heroContent.style.transition = 'opacity 0.25s ease, transform 0.25s ease';

      setTimeout(() => {
        if (heroSubtitle) heroSubtitle.textContent = slides[index].subtitle;
        if (heroTitle) heroTitle.textContent = slides[index].title;
        if (heroBtn) {
          heroBtn.textContent = slides[index].btnText;
          heroBtn.setAttribute('href', slides[index].link);
        }
        heroContent.style.opacity = '1';
        heroContent.style.transform = 'translateY(0)';
      }, 250);
    }

    const heroSlideBgs = document.querySelectorAll('.hero-slide-bg');
    if (heroSlideBgs.length > 0) {
      heroSlideBgs.forEach((bg, idx) => {
        const isActive = (idx === index);
        bg.classList.toggle('active', isActive);

        const vid = bg.querySelector('video');
        if (vid) {
          if (isActive) {
            vid.currentTime = 0;
            const playPromise = vid.play();
            if (playPromise !== undefined) {
              playPromise.catch(() => {});
            }
          } else {
            vid.pause();
          }
        }
      });
    }

    heroDots.forEach((dot, idx) => {
      dot.classList.toggle('active', idx === index);
    });
  }

  function startHeroTimer() {
    stopHeroTimer();
    heroTimer = setInterval(() => {
      const nextIdx = (currentHeroSlide + 1) % slides.length;
      updateHeroSlide(nextIdx);
    }, 3000);
  }

  function stopHeroTimer() {
    if (heroTimer) {
      clearInterval(heroTimer);
      heroTimer = null;
    }
  }

  function resetHeroTimer() {
    stopHeroTimer();
    startHeroTimer();
  }

  startHeroTimer();

  heroDots.forEach((dot, idx) => {
    dot.addEventListener('click', () => {
      updateHeroSlide(idx);
      resetHeroTimer();
    });
  });

  if (heroNext) {
    heroNext.addEventListener('click', () => {
      const nextIdx = (currentHeroSlide + 1) % slides.length;
      updateHeroSlide(nextIdx);
      resetHeroTimer();
    });
  }

  if (heroPrev) {
    heroPrev.addEventListener('click', () => {
      const prevIdx = (currentHeroSlide - 1 + slides.length) % slides.length;
      updateHeroSlide(prevIdx);
      resetHeroTimer();
    });
  }

  const chatBtn = document.querySelector('.chat-widget-btn');
  const chatDrawer = document.querySelector('.chat-drawer');
  const chatClose = document.querySelector('.chat-close-btn');

  if (chatBtn && chatDrawer) {
    chatBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      chatDrawer.classList.toggle('open');
    });

    if (chatClose) {
      chatClose.addEventListener('click', (e) => {
        e.stopPropagation();
        chatDrawer.classList.remove('open');
      });
    }

    document.addEventListener('click', (e) => {
      if (!chatDrawer.contains(e.target) && !chatBtn.contains(e.target)) {
        chatDrawer.classList.remove('open');
      }
    });
  }

  const searchBtn = document.querySelector('.btn-search');
  const searchModal = document.querySelector('.search-modal');
  const searchClose = document.querySelector('.search-close');

  if (searchBtn && searchModal) {
    searchBtn.addEventListener('click', () => {
      searchModal.classList.add('open');
      const searchInput = searchModal.querySelector('input');
      if (searchInput) searchInput.focus();
    });

    if (searchClose) {
      searchClose.addEventListener('click', () => {
        searchModal.classList.remove('open');
      });
    }
  }

  const mobileToggle = document.querySelector('.mobile-menu-toggle');
  const mobileNav = document.querySelector('.mobile-nav-drawer');
  const mobileClose = document.querySelector('.mobile-nav-close');
  const mobileBackdrop = document.querySelector('.mobile-nav-backdrop');

  function openMobileNav() {
    if (mobileNav) mobileNav.classList.add('open');
    if (mobileBackdrop) mobileBackdrop.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeMobileNav() {
    if (mobileNav) mobileNav.classList.remove('open');
    if (mobileBackdrop) mobileBackdrop.classList.remove('open');
    document.body.style.overflow = '';
  }

  if (mobileToggle) mobileToggle.addEventListener('click', openMobileNav);
  if (mobileClose) mobileClose.addEventListener('click', closeMobileNav);
  if (mobileBackdrop) mobileBackdrop.addEventListener('click', closeMobileNav);

  document.querySelectorAll('.mobile-nav-accordion-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const parent = btn.closest('.mobile-nav-accordion');
      if (parent) {
        parent.classList.toggle('active');
      }
    });
  });

  if (mobileNav) {
    mobileNav.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        closeMobileNav();
      });
    });
  }

  const addButtons = document.querySelectorAll('.product-add-btn');
  const cartCountEl = document.querySelector('.cart-count');
  let cartCount = 0;

  addButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      cartCount++;
      if (cartCountEl) {
        cartCountEl.textContent = cartCount;
        cartCountEl.style.transform = 'scale(1.35)';
        cartCountEl.style.backgroundColor = 'var(--color-peach-dark)';
        setTimeout(() => {
          cartCountEl.style.transform = 'scale(1)';
          cartCountEl.style.backgroundColor = 'var(--color-primary)';
        }, 300);
      }
      btn.textContent = 'ADDED TO BAG ✓';
      btn.style.backgroundColor = 'var(--color-primary)';
      btn.style.color = '#ffffff';
      setTimeout(() => {
        btn.textContent = 'ADD TO BAG';
        btn.style.backgroundColor = 'transparent';
        btn.style.color = 'var(--color-primary)';
      }, 1500);
    });
  });

  const togglePasswordBtn = document.getElementById('togglePasswordBtn');
  const passwordInput = document.getElementById('seller-password');
  if (togglePasswordBtn && passwordInput) {
    togglePasswordBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const isPassword = passwordInput.getAttribute('type') === 'password';
      passwordInput.setAttribute('type', isPassword ? 'text' : 'password');
      
      const eyeSlash = togglePasswordBtn.querySelector('.eye-slash');
      if (eyeSlash) {
        eyeSlash.style.display = isPassword ? 'block' : 'none';
      }
      togglePasswordBtn.setAttribute('aria-label', isPassword ? 'Hide password' : 'Show password');
    });
  }
});
