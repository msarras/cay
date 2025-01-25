const sidebar = document.getElementById('sidebar');

if (sidebar) {
    const toggleSidebarMobile = (sidebar, sidebarBackdrop) => {
        sidebar.classList.toggle('hidden');
        sidebarBackdrop.classList.toggle('hidden');
    }
    
    const toggleSidebarMobileEl = document.getElementById('toggleSidebarMobile');
    const sidebarBackdrop = document.getElementById('sidebarBackdrop');
    
    toggleSidebarMobileEl.addEventListener('click', () => {
        toggleSidebarMobile(sidebar, sidebarBackdrop);
    });
    
    sidebarBackdrop.addEventListener('click', () => {
        toggleSidebarMobile(sidebar, sidebarBackdrop);
    });
}
