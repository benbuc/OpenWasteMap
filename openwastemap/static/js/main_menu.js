function toggleMobileMenu() {
    var mobileNav = document.getElementById("mobile-nav")
    mobileNav.classList.toggle('active');
}

document.addEventListener("DOMContentLoaded", function(){
    var mobileMenuButton = document.getElementById("mobile-nav-button");
    mobileMenuButton.addEventListener("click", toggleMobileMenu);
});
