

let loading = true;

setTimeout(() => {
    loading = false;
}, 3000); 


function toggleLoadingBlur() {
    if (loading) {
        document.body.classList.add('blur');
    } else {
        document.body.classList.remove('blur');
    }
}

toggleLoadingBlur();

