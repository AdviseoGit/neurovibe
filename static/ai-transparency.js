/*
 * Injicerar AI-transparensraden i footern på sidor som saknar den.
 * Nya sidor har raden hårdkodad i HTML — detta är ett skyddsnät.
 */
document.addEventListener("DOMContentLoaded", function () {
    var footer = document.querySelector("footer");
    if (!footer) return;
    if (footer.innerHTML.indexOf("redaktionell-policy.html") !== -1) return;

    var container = footer.querySelector(".container") || footer;
    var p = document.createElement("p");
    p.className = "text-center text-sm text-gray-500 mt-4 border-t border-gray-800 pt-4";
    p.innerHTML = 'Innehållet produceras av AI-system inom mänskligt satta ramar och utgör ' +
        'inte medicinsk rådgivning &middot; ' +
        '<a href="/redaktionell-policy.html" class="underline hover:text-white">' +
        'Redaktionell policy &amp; källor</a>';
    container.appendChild(p);
});
