// Form validation 

// Get current and past date
var date = new Date();
var pastDate = new Date();

var pastYear = date.getFullYear() - 2;
pastDate.setFullYear(pastYear);

// Fill forms if necessary
var defaultValues = {
    ticker: 'AMZN',
    from_date: formatDate(pastDate),
    to_date: formatDate(date),
    ma1: 50,
    ma2: 100,
    symbol1: 'AMZN',
    symbol2: 'AAPL',
    symbol3: 'SPCE',
    symbol4: 'TSLA'
}

// Proper formatting
function formatDate(date){  
    var mnth = String(date.getMonth() + 1);
    var dy = String(date.getDate());
    var fy = date.getFullYear();
    var year = `${fy.toString().split('')[2]}${fy.toString().split('')[3]}`
    var dateStr = `${mnth}/${dy}/${year}`;
    return(dateStr);
}

// Fill in the blanks
document.querySelectorAll('input.form-control').forEach((input)=>{
    var id = input.id;
    if(input.value == ''){
        input.value = defaultValues[id];
    }
});


// Validation on dates
function validDate(){
    var fromDate = Date.parse(document.querySelector('#from_date').value);
    var toDate = Date.parse(document.querySelector('#to_date').value);
    var formatting = [document.querySelector('input#from_date'),document.querySelector('input#to_date')].filter(d=> d.value.includes('/')).length == 2;
    return fromDate <= toDate && formatting;
}

// Can't request future data
function dateCap(){
    return Date.parse(document.querySelector('#to_date').value) <= Date.parse(formatDate(date));
}

// No missing data
function filledInputs(){
missingInputs = 0;
document.querySelectorAll('.form-control').forEach((input)=>{
    if(input.value == '' || input.value == ' '){
        missingInputs = 1;
        return;
    }
})
return missingInputs == 0;
}


// Form validation
document.querySelector('button.button').addEventListener('click',(e)=>{
    e.preventDefault();
    if(! filledInputs()){
        alert('Please fill out each field');
        return;
    }
    if(! validDate()){
        alert('Invalid Date or Format!');
        return;
    }
    if(! dateCap()){
        alert('You cannot use a future date!');
        return;
    }
    if(validDate() && filledInputs()){
        // Set for dynamic URL (ONLY ON FORECAST PAGE)
        if(document.querySelector('div.analysis')){
            var inputTicker = document.querySelector('input#ticker').value;
            document.querySelector('form.data-form').setAttribute('action',`/prediction/${inputTicker}`);
        }

        document.querySelector('form.data-form').submit();
    }
    
});
