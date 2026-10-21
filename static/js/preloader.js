(function () {
    const LOADER_DURATION_MS = 2000;

    window.ClothifyLoader = window.ClothifyLoader || (function () {
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

    if (window.ClothifyLoader) {
        window.ClothifyLoader.start();
    }

    function dismissPreloaderSafely() {
        if (window.ClothifyLoader) {
            window.ClothifyLoader.done();
            setTimeout(() => {
                window.ClothifyLoader.hidePreloader();
            }, 250);
        }
    }

    setTimeout(dismissPreloaderSafely, LOADER_DURATION_MS);

    window.addEventListener('pageshow', function (event) {
        if (event.persisted && window.ClothifyLoader) {
            window.ClothifyLoader.done();
            window.ClothifyLoader.hidePreloader();
        }
    });
})();
