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
    var tr = event.target.closest('tr');

    var code = tr.querySelector('.tit').id;
    var coinName = tr.querySelector('.tit strong').textContent;
    var coinPrice = tr.querySelector('.price strong').textContent;

    var inputName = document.getElementById('in_name');
    inputName.value = coinName;

    var inputPrice = document.getElementById('in_price');
    inputPrice.value = parseFloat(coinPrice);


    // 차트
    let symbol = code.split('-')[1];
    changeSymbol(symbol);


    // 거래 내역
    fetch('history/' + code, {
        method: 'GET',
        headers: {
            'Content-type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {

            const hsHead = document.getElementById('history-head');
            const hsBody = document.getElementById('history-body');
            const hsEmpty = document.getElementById('history-empty');

            while (hsBody.firstChild) {
                hsBody.removeChild(hsBody.firstChild);
            }

            if (data.history.length > 0) {

                if (hsEmpty) {
                    hsEmpty.remove()
                }

                data.history.forEach(item => {
                    const tr = document.createElement('tr');
                    const td1 = document.createElement('td');
                    const td2 = document.createElement('td');
                    const td3 = document.createElement('td');
                    const td4 = document.createElement('td');

                    const divDate = document.createElement('div');
                    const divTime = document.createElement('div');

                    const divMarket = document.createElement('div');
                    const divType = document.createElement('div');

                    const divPrice = document.createElement('div');
                    const divTotal = document.createElement('div');

                    const divAmount = document.createElement('div');

                    divDate.setAttribute('font-size', '11px');
                    divDate.setAttribute('color', 'rgb(133, 139, 149)');
                    divDate.setAttribute('margin-bottom', '4px');
                    divTime.setAttribute('font-size', '11px');
                    divTime.setAttribute('color', 'rgb(133, 139, 149)');

                    divMarket.setAttribute('font-weight', '700');
                    divMarket.setAttribute('font-size', '12px');
                    divMarket.setAttribute('color', 'rgb(210, 212, 214)');
                    divMarket.setAttribute('text-align', 'center');
                    divMarket.setAttribute('margin-bottom', '4px');
                    divType.setAttribute('font-size', '12px');
                    divType.setAttribute('text-align', 'center');

                    divPrice.setAttribute('font-size', '12px');
                    divPrice.setAttribute('color', 'rgb(210, 212, 214)');
                    divPrice.setAttribute('margin-bottom', '4px');
                    divTotal.setAttribute('font-size', '12px');
                    divTotal.setAttribute('color', 'rgb(210, 212, 214)');

                    divAmount.setAttribute('font-size', '12px');
                    divAmount.setAttribute('color', 'rgb(210, 212, 214)');

                    divDate.textContent = moment(item.created_at).format("YYYY.MM.DD");
                    divTime.textContent = moment(item.created_at).format("HH:mm");
                    td1.appendChild(divDate);
                    td1.appendChild(divTime);

                    divMarket.textContent = item.market;
                    divType.textContent = item.side;
                    td2.appendChild(divMarket);
                    td2.appendChild(divType);

                    divPrice.textContent = parseFloat(item.price).toLocaleString();
                    divTotal.textContent = parseInt(item.total).toLocaleString();
                    td3.appendChild(divPrice);
                    td3.appendChild(divTotal);

                    divAmount.textContent = item.volume;
                    td4.appendChild(divAmount);

                    tr.appendChild(td1);
                    tr.appendChild(td2);
                    tr.appendChild(td3);
                    tr.appendChild(td4);

                    hsBody.appendChild(tr);
                });

            } else {
                if (!hsEmpty) {
                    const tr = document.createElement('tr');
                    const td = document.createElement('td');
                    const div = document.createElement('div');

                    tr.setAttribute('id', 'history-empty');
                    td.setAttribute('colspan', '4');

                    div.style.textAlign = 'center';
                    div.style.fontSize = '12px';
                    div.style.color = 'rgb(86, 93, 106)';
                    div.textContent = '체결 내역이 없습니다.';

                    tr.appendChild(td);
                    td.appendChild(div);
                    hsHead.insertAdjacentElement('afterend', tr);
                }
            }

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


const tickerSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/sml_trade/ticker/'
);


function sendTickerSignal() {
    tickerSocket.send(JSON.stringify({
        'signal': true,
    }));
}

let tkIntervalId;

tickerSocket.onopen = function (event) {
    tkIntervalId = setInterval(sendTickerSignal, 1000);
}


tickerSocket.onclose = function (event) {
    clearInterval(tkIntervalId);
}


tickerSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if (data.type == 'ticker') {
        data.value.forEach(item => {
            var code = document.getElementById(item.code);

            if (!code) {
                let tr = document.createElement('tr');

                let tdBookmark = document.createElement('td');
                let sbookmark = document.createElement('span');
                let abookmark = document.createElement('a');
                sbookmark.setAttribute('class', 'bookmark');
                abookmark.setAttribute('href', '#');
                sbookmark.appendChild(abookmark);
                tdBookmark.appendChild(sbookmark);

                let cAlign = document.createElement('td');
                cAlign.setAttribute('class', 'cAlign');

                // tit
                let tdTit = document.createElement('td');
                let aTit = document.createElement('a');
                let stTit = document.createElement('strong');
                let emTit = document.createElement('em');
                let sTit = document.createElement('span');

                let splitCode = item.code.split('-');

                tdTit.setAttribute('id', item.code);
                tdTit.setAttribute('class', 'tit');
                aTit.setAttribute('href', '#');
                stTit.textContent = item.name;
                emTit.textContent = splitCode[1];
                sTit.textContent = '/' + splitCode[0];

                aTit.appendChild(stTit);
                emTit.appendChild(sTit);
                tdTit.appendChild(aTit);
                tdTit.appendChild(emTit);

                // price
                let tdPrice = document.createElement('td');
                let stPrice = document.createElement('strong');
                let sPrice = document.createElement('span');
                tdPrice.setAttribute('class', 'price');
                sPrice.setAttribute('class', '');
                stPrice.textContent = item.trade_price;

                tdPrice.appendChild(stPrice);
                tdPrice.appendChild(sPrice);

                // percent
                let tdPercent = document.createElement('td');
                let pPercent = document.createElement('p');
                let emPercent = document.createElement('em');
                tdPercent.setAttribute('class', 'percent');
                pPercent.textContent = item.signed_change_rate;
                emPercent.textContent = item.signed_change_price;

                tdPercent.appendChild(pPercent);
                tdPercent.appendChild(emPercent);

                // rAlign
                let tdRightAlign = document.createElement('td');
                let tdRightP = document.createElement('p');
                let tdRightI = document.createElement('i');
                tdRightAlign.setAttribute('class', 'rAlign');
                tdRightP.textContent = parseInt((item.acc_trade_price_24h / 1_000_000)).toLocaleString();
                tdRightI.textContent = '백만';

                tdRightP.appendChild(tdRightI);
                tdRightAlign.appendChild(tdRightP);

                tr.appendChild(tdBookmark);
                tr.appendChild(cAlign);
                tr.appendChild(tdTit);
                tr.appendChild(tdPrice);
                tr.appendChild(tdPercent);
                tr.appendChild(tdRightAlign);

                var tableBody = document.querySelector('#market_list tbody');
                tableBody.appendChild(tr);
            } else {
                let coin = document.getElementById(item.code);

                let sPrice = coin.nextElementSibling;
                sPrice.querySelector('strong').innerHTML = item.trade_price;

                let pPercent = sPrice.nextElementSibling;
                pPercent.querySelector('p').innerHTML = item.signed_change_rate;
                pPercent.querySelector('em').innerHTML = item.signed_change_price;

                let tdRightP = pPercent.nextElementSibling;
                tdRightP.querySelector('p').innerHTML = parseInt((item.acc_trade_price_24h / 1_000_000)).toLocaleString() + '<i>백만</i>';
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


// TradingView
var widget = new TradingView.widget(
    {
        "autosize": true,
        "symbol": "UPBIT:BTCKRW",
        "interval": "1",
        "timezone": "Asia/Seoul",
        "theme": "dark",
        "style": "1",
        "locale": "kr",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_0e27d"
    }
);

function changeSymbol(code) {
    new TradingView.widget(
        {
            "autosize": true,
            "symbol": 'UPBIT:' + code + 'KRW',
            "interval": "1",
            "timezone": "Asia/Seoul",
            "theme": "dark",
            "style": "1",
            "locale": "kr",
            "enable_publishing": false,
            "hide_side_toolbar": false,
            "allow_symbol_change": true,
            "container_id": "tradingview_0e27d"
        }
    );
}