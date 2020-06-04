const hour = new Date().getHours();
const day = new Date().getDay();
const marketOpen = hour >= 6 && hour <= 16
&& day >= 1 && day <= 5;

if(marketOpen){
    console.log('Market is open!')
    // document.body.style.cssText 
}else{
    console.log('Market is closed');
    // document.body.style.background = '#333'
    // document.body.style.color = '#fff'
}

//tutor note:assuming you know what the running 20 day avg. and 200 day avg. is
function above_below(avg20d,avg200d){
    if (avg20d >avg200d){
        return"above: "+Math.abs(avg20d-avg200d)
    }else{
        return"below: "+Math.abs(avg20d-avg200d)
    }
}