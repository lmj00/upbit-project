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


var marketList = document.getElementById('market_list');

// 코인 클릭
marketList.addEventListener('click', function(event) {
    var target = event.target;
    var code = target.closest('tr');

    if (code) {
        var coinName = code.querySelector('.name').textContent;
        var coinPrice = code.querySelector('.price').textContent;

        var inputName = document.getElementById('in_name');
        inputName.value = coinName;

        var inputPrice = document.getElementById('in_price');
        inputPrice.value = parseFloat(coinPrice);
    }
});


// 코인 수량 입력
var inputQuantity = document.getElementById('in_quantity');
var inputPrice = document.getElementById('in_price');
var inputTotal = document.getElementById('in_total');

inputQuantity.addEventListener('input', function(event) {

    var quantity = parseFloat(event.target.value);
    var price = parseFloat(inputPrice.value);
    var total = quantity * price;

    inputTotal.value = isNaN(total) ? 0 : total.toLocaleString();
});


function order(event) {
    event.preventDefault();

    const form = document.getElementById('in_form');
    const formData = new FormData(form);
    const jsonData = {};


    for (let pair of formData.entries()) {
        jsonData[pair[0]] = pair[1];
    }

    const url = event.target.id === 'buyBtn' ? 'order/bid' : 'order/ask'

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

};

document.getElementById('buyBtn').addEventListener('click', order);
// document.getElementById('sellBtn').addEventListener('click', order); 


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

                var row = document.createElement('tr');

                row.appendChild(name);
                row.appendChild(price);

                var tableBody = document.querySelector('#market_list tbody');
                tableBody.appendChild(row);
            } else {

            }
        });
    } else if(data.type == 'sml_account') {
        const tableBody = document.getElementById('t-body');
        let tableHTML = '';
        
        data.value.forEach(item => {
            tableHTML += `
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
        
            tableBody.innerHTML = tableHTML;

    } else if (data.type == 'sml_account_balance') {
        const tableBody2 = document.getElementById('t-body2');
        const ac_dic = data.value;

        let tableHTML2 = '';
            tableHTML2 += `
            <tr>
                <td>${ac_dic.holding_krw}</td>
                <td>${ac_dic.total_assets}</td>
                <td>${ac_dic.total_purchase}</td>
                <td>${ac_dic.profit_or_loss}</td>
                <td>${ac_dic.total_evaluation}</td>
                <td>${ac_dic.rate_of_return}</td>
            </tr>
            `;

        tableBody2.innerHTML = tableHTML2;
    }
}