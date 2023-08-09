// static/js/floating-search.js

// Get the floating search bar element
const floatingSearchBar = document.getElementById('floating-search-bar');

// Set the scroll threshold to show/hide the floating search bar
const scrollThreshold = 200;

// Function to toggle the visibility of the floating search bar
function toggleFloatingSearchBar() {
    if (window.scrollY > scrollThreshold) {
        floatingSearchBar.style.display = 'block';
    } else {
        floatingSearchBar.style.display = 'none';
    }
}

// Add event listener to scroll event
window.addEventListener('scroll', toggleFloatingSearchBar);

// Call the function initially to set the initial state
toggleFloatingSearchBar();
