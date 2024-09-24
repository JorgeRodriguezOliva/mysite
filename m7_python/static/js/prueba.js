console.log("INIT - JS - DingDong ------->>>>>>");

function updateFilter(event, touch_is) {
    event.preventDefault();

    const form = document.getElementById("filters-form");
    form.submit();
}

console.log(`connect function - updateFilter ${updateFilter}`);