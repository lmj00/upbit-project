function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


// 코인 클릭
var marketList = document.getElementById('market_list');

marketList.addEventListener('click', function (event) {
    var target = event.target;
    var tr = target.closest('tr');

    var code = tr.querySelector('.name').id;
    var coinName = tr.querySelector('.name').textContent;
    var coinPrice = tr.querySelector('.price').textContent;

    var inputName = document.getElementById('in_name');
    inputName.value = coinName;

    var inputPrice = document.getElementById('in_price');
    inputPrice.value = parseFloat(coinPrice);

    fetch('history/' + code, {
        method: 'GET',
        headers: {
            'Content-type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {

        })
        .catch(error => {
            alert(error);
        });
        
});


// 코인 수량 입력
var inputQuantity = document.getElementById('in_quantity');
var inputPrice = document.getElementById('in_price');
var inputTotal = document.getElementById('in_total');

inputQuantity.addEventListener('input', function (event) {

    var quantity = parseFloat(event.target.value);
    var price = parseFloat(inputPrice.value);
    var total = quantity * price;

    inputTotal.value = isNaN(total) ? 0 : total.toLocaleString();
});


// 매수, 매도, 거래내역 버튼 클릭
const bid_btn = document.getElementById('bid');
const ask_btn = document.getElementById('ask');
const history_btn = document.getElementById('history');

const side_label = document.getElementById('side');
const trade_btn = document.getElementById('tradeBtn');
const in_form = document.getElementById('in_form');

const tableContainer = document.getElementById('history-table');


function toggleButtonAttributes(button, isActive) {
    button.removeAttribute('data-bs-toggle');
    button.removeAttribute('data-bs-target');
    button.removeAttribute('aria-controls');
    button.removeAttribute('aria-selected');
    button.classList.toggle('active', isActive);
}


bid_btn.addEventListener('click', function () {
    side_label.textContent = '매수가격(KRW)';
    trade_btn.textContent = '매수';
    trade_btn.dataset.type = 'bid';
    toggleButtonAttributes(ask_btn, false);
    toggleButtonAttributes(bid_btn, true);
    toggleButtonAttributes(history_btn, false);

    in_form.style.display = 'block';
    tableContainer.style.display = 'none';
});


ask_btn.addEventListener('click', function () {
    side_label.textContent = '매도가격(KRW)';
    trade_btn.textContent = '매도';
    trade_btn.dataset.type = 'ask';
    toggleButtonAttributes(ask_btn, true);
    toggleButtonAttributes(bid_btn, false);
    toggleButtonAttributes(history_btn, false);

    in_form.style.display = 'block';
    tableContainer.style.display = 'none';
});


history_btn.addEventListener('click', function () {
    toggleButtonAttributes(ask_btn, false);
    toggleButtonAttributes(bid_btn, false);
    toggleButtonAttributes(history_btn, true);
    in_form.style.display = 'none';
    tableContainer.style.display = 'block';
});


document.getElementById('tradeBtn').addEventListener('click', function (event) {
    event.preventDefault();

    const form = document.getElementById('in_form');
    const formData = new FormData(form);
    const jsonData = {};


    for (let pair of formData.entries()) {
        jsonData[pair[0]] = pair[1];
    }

    const url = event.target.dataset.type === 'bid' ? 'order/bid' : 'order/ask'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken
        },

        body: JSON.stringify(jsonData)
    })

        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })

        .catch(error => {
            alert("에러");
        });
});


const socket = new WebSocket(
    'ws://' + window.location.host + '/ws/sml_trade/'
);


function sendSignal() {
    socket.send(JSON.stringify({
        'signal': true,
    }));
}

let intervalId;

socket.onopen = function (event) {
    intervalId = setInterval(sendSignal, 1000);
}


socket.onclose = function (event) {
    clearInterval(intervalId);
}


socket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if (data.type == 'ticker') {
        data.value.forEach(item => {
            var code = document.getElementById(item.code);

            if (!code) {
                var name = document.createElement('td');
                name.setAttribute('id', item.code);
                name.setAttribute('class', 'name');
                name.textContent = item.name;

                var price = document.createElement('td');
                price.setAttribute('class', 'price');
                price.textContent = item.trade_price;
                
                var percent = document.createElement('td');
                percent.setAttribute('class', 'percent');
                
                var scpP = document.createElement('p');
                var scpEm = document.createElement('em');
                scpP.textContent = item.signed_change_rate;
                scpEm.textContent = item.signed_change_price;

                percent.appendChild(scpP);
                percent.appendChild(scpEm);

                var atp24h = document.createElement('td');
                atp24h.setAttribute('class', 'atp24h');
                atp24h.textContent = parseInt((item.acc_trade_price_24h / 1_000_000)).toLocaleString() + '백만';

                var row = document.createElement('tr');
                row.appendChild(name);
                row.appendChild(price);
                row.appendChild(percent);
                row.appendChild(atp24h);

                var tableBody = document.querySelector('#market_list tbody');
                tableBody.appendChild(row);
            } else {
                var price = code.nextElementSibling;
                var percent = price.nextElementSibling;
                var atp24h = percent.nextElementSibling;
                
                price.innerHTML = item.trade_price;
                percent.querySelector('p').innerHTML = item.signed_change_rate;
                percent.querySelector('em').innerHTML = item.signed_change_price;
                atp24h.innerHTML = parseInt(item.acc_trade_price_24h / 1_000_000).toLocaleString() + '백만';
            }
        });
    } else if (data.type == 'sml_account_balance') {
        const tableBody = document.getElementById('t-body');
        const ac_dic = data.value;

        let tableHTML = '';
        tableHTML += `
            <tr>
                <td>${ac_dic.holding_krw}</td>
                <td>${ac_dic.total_assets}</td>
                <td>${ac_dic.total_purchase}</td>
                <td>${ac_dic.profit_or_loss}</td>
                <td>${ac_dic.total_evaluation}</td>
                <td>${ac_dic.rate_of_return}</td>
            </tr>
            `;

        tableBody.innerHTML = tableHTML;

    } else if (data.type == 'sml_account') {
        const tableBody2 = document.getElementById('t-body2');
        let tableHTML2 = '';

        data.value.forEach(item => {
            tableHTML2 += `
                <tr style="border-bottom: 1px solid #ccc;">
                    <td>${item.name}</td>
                    <td>${item.balance}</td>
                    <td>${item.avg_buy_price}</td>
                    <td>${item.amount_money}</td>
                    <td>${item.valuation_amount}</td>
                    <td>${item.rate_of_return}</td>
                </tr>
            `;
        });

        tableBody2.innerHTML = tableHTML2;

    }
}