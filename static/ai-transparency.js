document.addEventListener("DOMContentLoaded", function() {
    const footer = document.querySelector("footer");
    if (footer) {
        // Kolla om texten redan finns, annars lägg till
        if (!footer.innerHTML.includes("Denna sajt skapas och drivs helt av AI")) {
             let container = footer.querySelector(".container") || footer;
             let p = document.createElement("p");
             p.className = "text-center text-sm text-gray-500 mt-4 border-t border-gray-800 pt-4";
             p.innerHTML = 'Denna sajt skapas och drivs helt av AI · <a href="/om-sajten.html" class="underline hover:text-white">Om sajten</a>';
             container.appendChild(p);
        }
    }
});
