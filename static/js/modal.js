(function() {
    console.log("Modal script loaded");

    function initModal() {
        const openBtn = document.getElementById('open-demo-modal');
        const closeBtn = document.getElementById('close-modal');
        const modal = document.getElementById('video-modal');
        const video = document.getElementById('demo-video');

        console.log("Initializing modal elements:", { openBtn, closeBtn, modal, video });

        if (!openBtn || !modal || !video) {
            console.error("Required modal elements missing from DOM");
            return;
        }

        const videoUrl = "https://www.youtube.com/embed/dQw4w9WgXcQ";

        function openModal() {
            console.log("Opening modal...");
            video.src = videoUrl;
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }

        function closeModal() {
            console.log("Closing modal...");
            modal.style.display = 'none';
            video.src = "";
            document.body.style.overflow = '';
        }

        openBtn.addEventListener('click', (e) => {
            e.preventDefault();
            openModal();
        });

        if (closeBtn) {
            closeBtn.addEventListener('click', closeModal);
        }

        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal();
            }
        });
    }

    // Ensure DOM is fully loaded before attempting to bind events
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initModal);
    } else {
        initModal();
    }
})();
