async function makeRequest(url, method) {
    console.log('1')
    let response = await fetch(url, method);
    console.log('2')
    if (response.ok) {
        console.log('3')
        return await response.json();
    } else {
        console.log('4')
        let error = new Error(response.statusText);
        error.response = response;
        throw error;
    }
}

function getCookie(cookieName){
    let cookie = {}
    document.cookie.split(";").forEach(function (el){
        let [key, value] = el.split("=");
        cookie[key.trim()] = value
    })
    return cookie[cookieName]
}

function removeDisplay(){
    var container = document.getElementById('container')
    while (container.firstChild) {
        container.removeChild(container.firstChild);
      }
}

function quoteRender(id, name, text, rate, email, date){
    let div = document.createElement('div')
    div.classList.add('mb-5')
    div.id = `${id}`


    let p_name = document.createElement('p')
    let a_text = document.createElement('a')
    let p_rate = document.createElement('p')
    let p_email = document.createElement('p')
    let p_date = document.createElement('p')
    p_name.innerText = `Имя автора ${name}`
    a_text.innerText = `${text}`
    a_text.href = `http://localhost:8000/api/${id}/detail`
    p_rate.innerText = `Оценка ${rate}`
    p_email.innerText = `Почта ${email}`
    p_date.innerText = `Дата создания ${date}`

    div.appendChild(p_name)
    div.appendChild(a_text)
    div.appendChild(p_rate)
    div.appendChild(p_email)
    div.appendChild(p_date)
    return div
}

function inputRender(value, inst=''){
    let input = document.createElement('input')
    input.id = value
    input.placeholder = value
    input.value = inst
    return input
}

function buttonRender(url, text){
    let button = document.createElement('button')
    button.innerText = text
    button.dataset['url'] = url
    return button
}

let listQuote = async function (event){
    removeDisplay()
    let url = event.target.dataset.quoteIndex
    let quotes = await makeRequest(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        }
    )
    container = document.getElementById('container')
    for (quote of quotes){
        q = quoteRender(quote.id, quote.name, quote.text, quote.rate, quote.email, quote.created_at)
        del_button = buttonRender(`api/${quote.id}/delete`, ' Удалить')
        upd_button = buttonRender(`${quote.id}`, ' Обновить')
        del_button.onclick = deleteQuote
        upd_button.onclick = updateQuoteForm
        container.appendChild(q)
        container.appendChild(del_button)
        container.appendChild(upd_button)
    }
}

let deleteQuote = async function(event){
    var url = event.target.dataset.url
    csrf_token = await makeRequest('http://localhost:8000/api/csrftoken')
    var csrf = getCookie('csrftoken')
    let quote = await makeRequest(url, {method: 'DELETE',
                                        body: {"delete" : "delete"},
                                        headers: {
                                            'Content-Type': 'application/json',
                                            'accept' : 'application/json',
                                            'X-CSRFToken': csrf
                                        }
                                        });
    removeDisplay()
    var container = document.getElementById('container')
    var h = document.createElement('h2')
    h.innerText = 'Цитата успешно удалена'
    container.appendChild(h)
}

let updateQuoteForm = async function (event){
    removeDisplay()
    var id = event.target.dataset.url
    var quote = await makeRequest(`/api/${id}/detail`)
    var fields = [{"name" : quote.name}, {"text" : quote.text}, {"email" : quote.email,}]
    var container = document.getElementById('container')
    for (field of fields){
        inp = inputRender(Object.keys(field)[0], Object.values(field)[0])
        container.appendChild(inp)
    }

    var button = buttonRender(`/api/${quote.id}/update/`, 'Изменить');
    button.onclick = updateQuote
    container.appendChild(button)
}

let updateQuote = async function(event){
    var url = event.target.dataset.url
    let name = document.getElementById('name').value
    let text = document.getElementById('text').value
    let email = document.getElementById('email').value
    let info = {
        "name": name,
        "text": text,
        "email": email
    }
    csrf_token = await makeRequest('http://localhost:8000/api/csrftoken')
    var csrf = getCookie('csrftoken')
    let quote = await makeRequest(url, {method: 'PUT',
                                        body: JSON.stringify(info),
                                        headers: {
                                            'Content-Type': 'application/json',
                                            'accept' : 'application/json',
                                            'X-CSRFToken': csrf
                                        }
                                        });
    removeDisplay()
    var container = document.getElementById('container')
    var h = document.createElement('h2')
    h.innerText = 'Цитата успешно обновлена'
    q = quoteRender(quote.id, quote.name, quote.text, quote.rate, quote.email, quote.created_at)
    container.appendChild(h)
    container.appendChild(q)
}

let createQuoteForm = function (){
    removeDisplay()
    var fields = ['name', 'text', 'email']
    var container = document.getElementById('container')
    for (field of fields){
        inp = inputRender(field)
        container.appendChild(inp)
    }
    var button = buttonRender('/api/create/', 'Создать');
    button.onclick = createQuote
    container.appendChild(button)
}

let createQuote = async function (event){
    let url = event.target.dataset.url
    let name = document.getElementById('name').value
    let text = document.getElementById('text').value
    let email = document.getElementById('email').value
    let info = {
        "name": name,
        "text": text,
        "email": email
    }
    csrf_token = await makeRequest('http://localhost:8000/api/csrftoken')
    var csrf = getCookie('csrftoken')
    let quote = await makeRequest(url, {method: 'POST',
                                        body: JSON.stringify(info),
                                        headers: {
                                            'Content-Type': 'application/json',
                                            'accept' : 'application/json',
                                            'X-CSRFToken': csrf
                                        }
                                        });
    removeDisplay()
    var container = document.getElementById('container')
    var h = document.createElement('h2')
    h.innerText = 'Цитата успешно добавлена'
    q = quoteRender(quote.id, quote.name, quote.text, quote.rate, quote.email, quote.created_at)
    container.appendChild(h)
    container.appendChild(q)
    }

let display = async function (){
    let quotes = await makeRequest('http://localhost:8000/api/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        }
    )
    container = document.getElementById('container')
    for (quote of quotes){
        q = quoteRender(quote.id, quote.name, quote.text, quote.rate, quote.email, quote.created_at)
        del_button = buttonRender(`api/${quote.id}/delete`, ' Удалить')
        upd_button = buttonRender(`${quote.id}`, ' Обновить')
        del_button.onclick = deleteQuote
        upd_button.onclick = updateQuoteForm
        container.appendChild(q)
        container.appendChild(del_button)
        container.appendChild(upd_button)
    }
}

display()