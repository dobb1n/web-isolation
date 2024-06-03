/* ****************************************************************************
 *
 *   SPA router
 *   =====================
 * 
 *   The router allows for the URL in the address bar to be updated as
 *   users navigate around different functionality on the system. This 
 *   means that users can link back to specific pages, can share links
 *   and things like help pages can link to other places in help pages.
 * 
 *   This implementation is a hash-based SPA, this means that the URL
 *   is split in two by a hash (#), the part before the hash is the
 *   page retrieved from the server, the part after the hash is the
 *   part served by the router.
 *
 **************************************************************************** */

// Create the route definitions with the default route
var routes = [
    { route: "home", content_url: "/assets/templates/home.html" },
    { route: "second", content_url: "/assets/templates/second.html" }
];

// default to an invalid route so we have to route on load
var current_route = "$"; 

var setInnerHtml = function(elm, html, route) {
    elm.insertAdjacentHTML('beforeEnd', `<div class="module" route="${route}" id="route-${route}">${html}</div>`);
    new_route = document.getElementById(`route-${route}`);
    Array.from(new_route.querySelectorAll("script")).forEach(oldScript => {
        const newScript = document.createElement("script");
        Array.from(oldScript.attributes)
            .forEach(attr => newScript.setAttribute(attr.name, attr.value));
        newScript.appendChild(document.createTextNode(oldScript.innerHTML));
        oldScript.parentNode.replaceChild(newScript, oldScript);
    });
}

function setVisibility(elem, visibile) {
    if (visibile) {
        if (elem.classList.contains("d-none")) {
            elem.classList.remove("d-none")
        }
    } else {
        if (!elem.classList.contains("d-none")) {
            elem.classList.add("d-none")
        }
    }
}

// Load the content of the page
function renderRoute(url, old_route, new_route) {

    // if we're not routing, quit now
    if (old_route == new_route) { return; }

    // Hide the current route, this gives two benefits:
    // - we only need to load each route once
    // - we don't need to track unsaved state
    old_module = document.querySelectorAll(`[route='${old_route}']`);
    if (old_module.length == 1) {
        setVisibility(old_module[0], false);
    }

    // if we've loaded this page before, we only want to unhide the page
    new_module = document.querySelectorAll(`[route='${new_route}']`);
    if (new_module.length == 1) {
        setVisibility(new_module[0], true);
        return;
    }

    const doRouting = async() => {
        // if this is the first time we need to load this route, fetch the content
        const response = await fetch(url);
        const body = await response.text();
        setInnerHtml(document.getElementById("page-container"), body, new_route);
    }
    doRouting();
};

// Perform the routing
function Routing() {
    const new_route = window.location.hash.replace(/^#\//, "").split('?')[0];
    // The default route is first registered route (home)
    let route = routes[0];
    // Find matching route
    for (let index = 0; index < routes.length; index++) {
        let testRoute = routes[index];
        if (new_route == testRoute.route) {
            route = testRoute;
        }
    }
    // Load the route
    renderRoute(route.content_url, current_route, route.route);
    current_route = route.route;
}

// create a listener for changes to the URL
window.addEventListener('popstate', Routing);
