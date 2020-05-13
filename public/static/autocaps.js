
var inputs = document.querySelectorAll('input#ticker');
inputs.forEach((input)=>{
    input.addEventListener('input',(e)=>{
        e.target.value = e.target.value.toUpperCase();
    })
});