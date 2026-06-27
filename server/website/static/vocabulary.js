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
        const char = this.textContent;
        const match = kanjis.find(k => k.kanji_char === char)

        if (match){
            let id = match.id;
            const page = Math.ceil(id / 50);
            //Allow to add a class which I defined a specific style on CSS
            span.classList.add('kanji-match');

            span.addEventListener('mouseenter', function(){
                //Show preview of kanji with its reading and meaning
                showPreview(span, id);
            });

            span.addEventListener('mouseout', function(){
                span.classList.remove('kanji-match');
                removePreview();
            });

            //Go to the kanji-list page exactly where that kanji is located
            span.addEventListener('click', function() {
            window.location.href = '/kanji-list?page=' + page + '#' + char;
            });
        }
    });
});

function showPreview(span, matchId) {
    my_kanji = kanjis.find(k => k.id === matchId)
    meaning = my_kanji.meaning;
    reading = my_kanji.reading;
    const preview = document.getElementById('kanji-preview');
    const rect = span.getBoundingClientRect();
    preview.style.top = (rect.top + window.scrollY - preview.offsetHeight - 10) + 'px';
    preview.style.left = (rect.left + window.scrollX) + 'px';
    preview.innerHTML = reading + '<br>' + meaning;
    preview.classList.add('visible');
}

function removePreview(){
    document.getElementById('kanji-preview').classList.remove('visible');
}