function addParams(list){
    const currentUrl = new URL(window.location.href);
    for (let param of list){
        const [key, value] = param;
        currentUrl.searchParams.set(key, value);
    }
    window.location.href = currentUrl.toString();
}

function addParam(key, value){
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set(key, value);
    window.location.href = currentUrl.toString();
}

function chechboxClicked(chechbox){
    event.preventDefault();
    const field = $(chechbox).attr("id");
    addParam(field, chechbox.checked);
}
