
    var inputIds = ['ticker','symbol1','symbol2','symbol3','symbol4']
    document.querySelectorAll('input').forEach((input)=>{
        if(inputIds.includes(input.id)){
            input.addEventListener('input',(e)=>{
               e.target.value = e.target.value.toUpperCase();
            })
        }
    });