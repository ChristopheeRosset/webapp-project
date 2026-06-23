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
            if (kanjis.includes(char)){
                console.log(char);
                span.addEventListener('click', function() {
                    window.location.href = '/kanji-list#' + char;
                });
            }
        });
    });
});