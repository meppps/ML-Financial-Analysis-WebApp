
// +/- colors for nums
document.querySelectorAll('td').forEach((td)=>{
    if(td.innerText == 'NaN'){
        td.parentElement.style.display='none';
    }
    if(td.innerText == 'Bullish'){
        td.style.color = 'green'
    }else if(td.innerText == 'Bearish'){
        td.style.color = 'red'
    }
    if(td.innerText.endsWith('%')){
        if(td.innerText.startsWith('-')){
            td.style.color = 'red'
        }else{
            td.style.color = 'green'
        }
    }
});


document.querySelector('table.dataframe').clientWidth = document.querySelector('table#analysisOne').clientWidth;