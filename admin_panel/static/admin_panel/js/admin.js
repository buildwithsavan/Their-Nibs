window.ClothifyLoader = (function () {
    let progressTimer = null;
    let currentProgress = 0;

    function getProgressBar() {
        return document.getElementById('clothifyTopProgress');
    }

    function getPreloader() {
        return document.getElementById('clothifyPageLoader');
    }

    return {

        start: function () {
            const bar = getProgressBar();
            if (!bar) return;

            clearInterval(progressTimer);
            bar.classList.remove('finished');
            bar.classList.add('active');
            currentProgress = 15;
            bar.style.width = currentProgress + '%';

            progressTimer = setInterval(() => {
                if (currentProgress < 70) {
                    currentProgress += Math.random() * 12 + 6;
                } else if (currentProgress < 90) {
                    currentProgress += Math.random() * 3 + 1;
                }
                bar.style.width = Math.min(currentProgress, 92) + '%';
            }, 180);
        },

        done: function () {
            const bar = getProgressBar();
            if (!bar) return;

            clearInterval(progressTimer);
            currentProgress = 100;
            bar.style.width = '100%';
            bar.classList.add('finished');

            setTimeout(() => {
                bar.classList.remove('active', 'finished');
                bar.style.width = '0%';
                currentProgress = 0;
            }, 400);
        },

        hidePreloader: function () {
            const loader = getPreloader();
            if (loader && !loader.classList.contains('fade-out')) {
                loader.classList.add('fade-out');
            }
        },

        showPreloader: function (statusText) {
            const loader = getPreloader();
            if (loader) {
                if (statusText) {
                    const statusElem = document.getElementById('preloaderStatusText');
                    if (statusElem) statusElem.innerText = statusText;
                }
                loader.classList.remove('fade-out');
            }
        }
    };
})();

const ADMIN_LOADER_DURATION_MS = 2000;

function dismissPreloaderSafely() {
    window.ClothifyLoader.done();
    setTimeout(() => {
        window.ClothifyLoader.hidePreloader();
    }, 250);
}

setTimeout(dismissPreloaderSafely, ADMIN_LOADER_DURATION_MS);

window.addEventListener('pageshow', function () {
    window.ClothifyLoader.done();
    window.ClothifyLoader.hidePreloader();
    document.querySelectorAll('.btn-loading').forEach(btn => {
        btn.classList.remove('btn-loading');
        btn.removeAttribute('disabled');
    });
});

document.addEventListener('DOMContentLoaded', function () {
    
    function getCsrfToken() {
        const input = document.querySelector('[name=csrfmiddlewaretoken]');
        if (input && input.value) return input.value;
        const name = 'csrftoken';
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    return decodeURIComponent(cookie.substring(name.length + 1));
                }
            }
        }
        return '';
    }

    document.querySelectorAll('a[href]').forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            const target = this.getAttribute('target');
            if (
                href &&
                !href.startsWith('#') &&
                !href.startsWith('javascript:') &&
                !href.startsWith('mailto:') &&
                !href.startsWith('tel:') &&
                target !== '_blank' &&
                !e.ctrlKey &&
                !e.metaKey &&
                !e.shiftKey
            ) {
                window.ClothifyLoader.start();
            }
        });
    });

    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function (e) {
            if (e.defaultPrevented) return;
            const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn && !submitBtn.classList.contains('no-loader')) {
                submitBtn.classList.add('btn-loading');
                window.ClothifyLoader.start();
            }
        });
    });

    const userPill = document.querySelector('.topbar-user-pill');
    const userDropdown = document.querySelector('.topbar-user-dropdown');
    if (userPill && userDropdown) {
        userPill.addEventListener('click', (e) => {
            e.stopPropagation();
            userDropdown.classList.toggle('show');
        });
        document.addEventListener('click', () => {
            userDropdown.classList.remove('show');
        });
    }

    const togglePassBtns = document.querySelectorAll('.toggle-password-btn');
    togglePassBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.dataset.target || 'login-password';
            const input = document.getElementById(targetId);
            if (input) {
                if (input.type === 'password') {
                    input.type = 'text';
                    btn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>`;
                } else {
                    input.type = 'password';
                    btn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>`;
                }
            }
        });
    });

    const confirmActions = document.querySelectorAll('[data-confirm]');
    confirmActions.forEach(element => {
        element.addEventListener('click', (e) => {
            const message = element.getAttribute('data-confirm') || 'Are you sure you want to proceed?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    window.openQuickStockModal = function (productId, productName, currentStock) {
        const modalBackdrop = document.getElementById('stockModalBackdrop');
        if (!modalBackdrop) return;
        const idInput = document.getElementById('stockModalProdId');
        const nameElem = document.getElementById('stockModalProdName');
        const stockInput = document.getElementById('stockModalStockInput');

        if (idInput) idInput.value = productId;
        if (nameElem) nameElem.innerText = productName;
        if (stockInput) {
            stockInput.value = currentStock;
            setTimeout(() => stockInput.focus(), 50);
        }
        modalBackdrop.style.display = 'flex';
    };

    window.closeQuickStockModal = function () {
        const modalBackdrop = document.getElementById('stockModalBackdrop');
        if (modalBackdrop) modalBackdrop.style.display = 'none';
    };

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            window.closeQuickStockModal();
        }
    });
    const modalBackdrop = document.getElementById('stockModalBackdrop');
    if (modalBackdrop) {
        modalBackdrop.addEventListener('click', (e) => {
            if (e.target === modalBackdrop) {
                window.closeQuickStockModal();
            }
        });
    }

    const stockForm = document.getElementById('quickStockForm');
    if (stockForm) {
        stockForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const prodId = document.getElementById('stockModalProdId').value;
            const newStock = document.getElementById('stockModalStockInput').value;
            const submitBtn = stockForm.querySelector('button[type="submit"]');
            const token = getCsrfToken();

            submitBtn.disabled = true;
            submitBtn.innerText = 'Saving...';
            window.ClothifyLoader.start();

            try {
                const formData = new FormData();
                formData.append('product_id', prodId);
                formData.append('stock', newStock);

                const response = await fetch('/admin-panel/api/inventory/quick-update/', {
                    method: 'POST',
                    headers: { 'X-CSRFToken': token },
                    body: formData
                });
                const data = await response.json();
                if (data.success) {
                    const stockCell = document.querySelector(`.stock-val-${prodId}`);
                    if (stockCell) stockCell.innerText = data.stock;
                    window.closeQuickStockModal();
                    window.location.reload();
                } else {
                    alert('Error updating stock: ' + data.message);
                }
            } catch (err) {
                alert('Request failed: ' + err);
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerText = 'Save Stock';
                window.ClothifyLoader.done();
            }
        });
    }

    const imgUrlInput = document.querySelector('#productForm input[name="image_url"]');
    const imgPreview = document.getElementById('imagePreview');
    const imgPlaceholder = document.getElementById('imagePlaceholder');
    const imgContainer = document.getElementById('imagePreviewContainer');

    if (imgUrlInput) {
        imgUrlInput.addEventListener('input', function () {
            const url = this.value.trim();
            if (url) {
                if (imgPreview) {
                    imgPreview.src = url;
                    imgPreview.style.display = 'inline-block';
                    if (imgPlaceholder) imgPlaceholder.style.display = 'none';
                } else if (imgContainer) {
                    imgContainer.innerHTML = `<img id="imagePreview" src="${url}" alt="Preview" style="max-width: 100%; height: 200px; object-fit: cover; border-radius: 8px; border: 1px solid var(--border-subtle);">`;
                }
            } else {
                if (imgPreview) imgPreview.style.display = 'none';
                if (imgPlaceholder) imgPlaceholder.style.display = 'flex';
            }
        });
    }

    const alerts = document.querySelectorAll('.clothify-alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.4s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 400);
        }, 5000);
    });

    const adminSidebarToggle = document.getElementById('adminSidebarToggle');
    const adminSidebar = document.querySelector('.admin-sidebar');
    const adminBackdrop = document.getElementById('adminSidebarBackdrop');

    if (adminSidebarToggle && adminSidebar) {
        adminSidebarToggle.addEventListener('click', function (e) {
            e.stopPropagation();
            const isOpen = adminSidebar.classList.toggle('show');
            if (adminBackdrop) adminBackdrop.classList.toggle('show', isOpen);
            document.body.style.overflow = isOpen ? 'hidden' : '';
        });
    }

    const adminCloseBtn = document.getElementById('adminSidebarClose');
    if (adminBackdrop) {
        adminBackdrop.addEventListener('click', function () {
            if (adminSidebar) adminSidebar.classList.remove('show');
            adminBackdrop.classList.remove('show');
            document.body.style.overflow = '';
        });
    }

    if (adminCloseBtn) {
        adminCloseBtn.addEventListener('click', function () {
            if (adminSidebar) adminSidebar.classList.remove('show');
            if (adminBackdrop) adminBackdrop.classList.remove('show');
            document.body.style.overflow = '';
        });
    }

    if (adminSidebar) {
        adminSidebar.querySelectorAll('.menu-item').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 1024) {
                    adminSidebar.classList.remove('show');
                    if (adminBackdrop) adminBackdrop.classList.remove('show');
                    document.body.style.overflow = '';
                }
            });
        });
    }

    const notifBellBtn = document.getElementById('notifBellBtn');
    const notifDropdown = document.getElementById('notifDropdown');
    const userDropdownElem = document.querySelector('.topbar-user-dropdown');

    if (notifBellBtn && notifDropdown) {
        notifBellBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            if (userDropdownElem) userDropdownElem.classList.remove('show');
            const isShown = notifDropdown.classList.toggle('show');
            notifBellBtn.setAttribute('aria-expanded', isShown);
        });

        document.addEventListener('click', function (e) {
            if (!notifDropdown.contains(e.target) && !notifBellBtn.contains(e.target)) {
                notifDropdown.classList.remove('show');
                notifBellBtn.setAttribute('aria-expanded', 'false');
            }
        });
    }

    function updateNotifBadges(newCount) {
        const pulse = document.getElementById('notifPulse');
        const badge = document.getElementById('notifBadge');
        const headerCount = document.getElementById('notifHeaderCount');
        const markAllBtn = document.getElementById('markAllReadBtn');

        if (newCount <= 0) {
            if (pulse) pulse.style.display = 'none';
            if (badge) badge.style.display = 'none';
            if (headerCount) headerCount.style.display = 'none';
            if (markAllBtn) markAllBtn.style.display = 'none';
        } else {
            if (pulse) pulse.style.display = 'block';
            if (badge) {
                badge.innerText = newCount;
                badge.style.display = 'flex';
            }
            if (headerCount) {
                headerCount.innerText = newCount + ' new';
                headerCount.style.display = 'inline-block';
            }
        }
    }

    const markAllBtn = document.getElementById('markAllReadBtn');
    if (markAllBtn) {
        markAllBtn.addEventListener('click', async function () {
            const token = getCsrfToken();
            markAllBtn.style.opacity = '0.5';
            markAllBtn.style.pointerEvents = 'none';

            try {
                const res = await fetch('/admin-panel/api/notifications/mark-all-read/', {
                    method: 'POST',
                    headers: { 'X-CSRFToken': token }
                });
                const data = await res.json();
                if (data.success) {
                    updateNotifBadges(0);
                    const container = document.getElementById('notifListContainer');
                    if (container) {
                        container.innerHTML = `
                            <div class="notif-empty-state">
                                <div class="notif-empty-icon">✓</div>
                                <div class="notif-empty-title">All caught up!</div>
                                <div class="notif-empty-subtitle">You have no unread notifications right now.</div>
                            </div>
                        `;
                    }
                }
            } catch (err) {
                console.error('Failed to mark all notifications read:', err);
            } finally {
                markAllBtn.style.opacity = '1';
                markAllBtn.style.pointerEvents = 'auto';
            }
        });
    }

    window.markNotifReadFromFlyout = async function (notifId, el) {
        const token = getCsrfToken();
        const item = el.closest('.notif-dropdown-item');
        if (item) {
            item.style.transition = 'all 0.25s ease';
            item.style.opacity = '0';
            item.style.transform = 'translateX(20px)';
        }

        try {
            const formData = new FormData();
            formData.append('notification_id', notifId);
            const res = await fetch('/admin-panel/api/notifications/mark-read/', {
                method: 'POST',
                headers: { 'X-CSRFToken': token },
                body: formData
            });
            const data = await res.json();
            if (data.success) {
                if (item) item.remove();
                if (typeof data.unread_count !== 'undefined') {
                    updateNotifBadges(data.unread_count);
                    if (data.unread_count === 0) {
                        const container = document.getElementById('notifListContainer');
                        if (container) {
                            container.innerHTML = `
                                <div class="notif-empty-state">
                                    <div class="notif-empty-icon">✓</div>
                                    <div class="notif-empty-title">All caught up!</div>
                                    <div class="notif-empty-subtitle">You have no unread notifications right now.</div>
                                </div>
                            `;
                        }
                    }
                }
            }
        } catch (e) {
            console.error('Failed to mark notification read:', e);
            if (item) {
                item.style.opacity = '1';
                item.style.transform = 'none';
            }
        }
    };

    window.markNotifRead = async function (notifId, el) {
        const token = getCsrfToken();
        try {
            const formData = new FormData();
            formData.append('notification_id', notifId);
            await fetch('/admin-panel/api/notifications/mark-read/', {
                method: 'POST',
                headers: { 'X-CSRFToken': token },
                body: formData
            });
            if (el) el.closest('.notif-item').classList.add('read');
        } catch (e) { }
    };

    window.ClothifyLightbox = (function () {
        let gallery = [];
        let currentIndex = 0;

        const backdrop = document.getElementById('clothifyLightboxBackdrop');
        const imgEl = document.getElementById('clothifyLightboxImg');
        const titleEl = document.getElementById('clothifyLightboxTitle');
        const subtitleEl = document.getElementById('clothifyLightboxSubtitle');
        const counterEl = document.getElementById('clothifyLightboxCounter');
        const newTabBtn = document.getElementById('lightboxNewTabBtn');
        const prevBtn = document.getElementById('clothifyLightboxPrev');
        const nextBtn = document.getElementById('clothifyLightboxNext');
        const closeBtn = document.getElementById('clothifyLightboxClose');

        function updateView() {
            if (!gallery.length || currentIndex < 0 || currentIndex >= gallery.length) return;
            const item = gallery[currentIndex];

            if (imgEl) {
                imgEl.src = item.src;
                imgEl.alt = item.title || 'Product Preview';
            }

            if (titleEl) titleEl.textContent = item.title || 'Garment Preview';
            if (subtitleEl) subtitleEl.textContent = item.subtitle || '';
            if (newTabBtn) newTabBtn.href = item.src;

            if (counterEl) {
                counterEl.textContent = gallery.length > 1 ? `${currentIndex + 1} of ${gallery.length}` : '';
            }

            if (prevBtn) {
                prevBtn.style.display = gallery.length > 1 ? 'inline-block' : 'none';
                prevBtn.disabled = currentIndex === 0;
                prevBtn.style.opacity = currentIndex === 0 ? '0.4' : '1';
            }
            if (nextBtn) {
                nextBtn.style.display = gallery.length > 1 ? 'inline-block' : 'none';
                nextBtn.disabled = currentIndex === gallery.length - 1;
                nextBtn.style.opacity = currentIndex === gallery.length - 1 ? '0.4' : '1';
            }
        }

        function open(options) {
            if (!backdrop) return;
            gallery = options.gallery && options.gallery.length ? options.gallery : [{
                src: options.src,
                title: options.title || 'Garment Preview',
                subtitle: options.subtitle || ''
            }];
            currentIndex = Math.max(0, Math.min(options.index || 0, gallery.length - 1));

            backdrop.classList.add('active');
            backdrop.setAttribute('aria-hidden', 'false');
            document.body.style.overflow = 'hidden';

            updateView();
        }

        function close() {
            if (!backdrop) return;
            backdrop.classList.remove('active');
            backdrop.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
        }

        function next() {
            if (currentIndex < gallery.length - 1) {
                currentIndex++;
                updateView();
            }
        }

        function prev() {
            if (currentIndex > 0) {
                currentIndex--;
                updateView();
            }
        }

        if (closeBtn) closeBtn.addEventListener('click', close);
        if (prevBtn) prevBtn.addEventListener('click', prev);
        if (nextBtn) nextBtn.addEventListener('click', next);

        if (backdrop) {
            backdrop.addEventListener('click', function (e) {
                if (e.target === backdrop) {
                    close();
                }
            });
        }

        document.addEventListener('keydown', function (e) {
            if (!backdrop || !backdrop.classList.contains('active')) return;
            if (e.key === 'Escape') {
                close();
            } else if (e.key === 'ArrowRight') {
                next();
            } else if (e.key === 'ArrowLeft') {
                prev();
            }
        });

        return {
            open: open,
            close: close,
            next: next,
            prev: prev
        };
    })();

    document.addEventListener('click', function (e) {
    
        const trigger = e.target.closest('[data-lightbox-src], .lightbox-trigger, .product-thumb-container, .clothify-table td img, #imagePreview, .preview-zoomable-img, .reviewed-garment-thumb, .reviewed-garment-box img');
        if (!trigger) return;

        if (trigger.classList.contains('user-avatar') && !trigger.hasAttribute('data-lightbox-src')) return;
        if (trigger.src && trigger.src.includes('ui-avatars.com')) return;

        e.preventDefault();
        e.stopPropagation();

        const clickedSrc = trigger.getAttribute('data-lightbox-src') || (trigger.tagName === 'IMG' ? trigger.src : trigger.querySelector('img')?.src);
        if (!clickedSrc || clickedSrc.trim() === '' || clickedSrc === '#' || clickedSrc.includes('javascript:')) return;

        const title = trigger.getAttribute('data-lightbox-title') || 
                      trigger.getAttribute('data-title') ||
                      trigger.getAttribute('alt') || 
                      trigger.closest('tr')?.querySelector('strong')?.textContent?.trim() || 
                      'Garment Preview';

        const subtitle = trigger.getAttribute('data-lightbox-subtitle') || 
                         trigger.getAttribute('data-category') ||
                         trigger.closest('tr')?.querySelector('[style*="monospace"]')?.textContent?.trim() || 
                         '';

        const allTriggers = Array.from(document.querySelectorAll('.clothify-table tbody tr [data-lightbox-src], .clothify-table tbody tr td img'));
        let gallery = [];
        let activeIndex = 0;

        if (allTriggers.length > 1) {
            allTriggers.forEach((el) => {
                const src = el.getAttribute('data-lightbox-src') || (el.tagName === 'IMG' ? el.src : el.querySelector('img')?.src);
                if (src && !src.includes('ui-avatars.com')) {
                    const itemTitle = el.getAttribute('data-lightbox-title') || 
                                     el.getAttribute('alt') || 
                                     el.closest('tr')?.querySelector('strong')?.textContent?.trim() || 
                                     'Garment';
                    const itemSub = el.getAttribute('data-lightbox-subtitle') || 
                                    el.closest('tr')?.querySelector('[style*="monospace"]')?.textContent?.trim() || 
                                    '';
                    gallery.push({
                        src: src,
                        title: itemTitle,
                        subtitle: itemSub
                    });
                }
            });
            activeIndex = gallery.findIndex(item => item.src === clickedSrc);
            if (activeIndex === -1) activeIndex = 0;
        } else {
            gallery = [{ src: clickedSrc, title: title, subtitle: subtitle }];
            activeIndex = 0;
        }

        window.ClothifyLightbox.open({
            gallery: gallery,
            index: activeIndex,
            src: clickedSrc,
            title: title,
            subtitle: subtitle
        });
    });
});


