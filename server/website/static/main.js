//Get kanji list
let kanjis = [];

fetch('/kanji-chars')
    .then (res => res.json())
    .then (data => {
        kanjis = data;
    });

document.getElementById('edit-btn').addEventListener('click', function() {
    document.querySelectorAll('.display-field').forEach(span => {
        span.style.display = 'none';
    });
    document.querySelectorAll('.editable-field').forEach(input => {
        input.style.display = 'block';
    });
});

//Link from voc word to Kanji List if that kanji has already been added
document.querySelectorAll('.jap-word').forEach(span => { 
    span.addEventListener('mouseover', function() { 
        const word = this.textContent.split('');
        //console.log(word); can be checked on the browser console

        //Check every char of the the first vocabulary column
        word.forEach(char => {
            const match = kanjis.find(k => k.character === char)
            if (match){
                const page = Math.ceil(match.id / 100);
                //Allow to add a class which I defined a specific style on CSS
                span.classList.add('kanji-match');
                
                span.addEventListener('mouseout', function(){
                    span.classList.remove('kanji-match');
                });
                span.addEventListener('click', function() {
                window.location.href = '/kanji-list?page=' + page + '#' + char;
                });
            }
        });
    });
});