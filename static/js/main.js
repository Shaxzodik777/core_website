const grid1 = document.querySelector('#grid_1');
const grid3 = document.querySelector('#grid_3');

let articles = document.querySelectorAll('.article-item')

grid1.addEventListener('click', () => {
    articles.forEach(article => {
        if (article.classList.contains('col-md-6')) {
            article.classList.remove('col-md-6')
            article.classList.add('col-md-12')
        } else {
            article.classList.remove('col-md-12')
            article.classList.add('col-md-6')
        }
    })
})

grid3.addEventListener('click', () => {
    articles.forEach(article => {
        if (article.classList.contains('col-md-6') || article.classList.contains('col-md-12')) {
            article.classList.remove('col-md-6')
            article.classList.remove('col-md-12')
            article.classList.add('col-md-4')
        } else {
            article.classList.remove('col-md-4')
            article.classList.add('col-md-6')
        }
    })
})