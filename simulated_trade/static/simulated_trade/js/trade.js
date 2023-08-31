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


    // 즐겨찾기
    const bookmarkContainer = event.target.closest('.bookmark');
    
    if (bookmarkContainer) {
        const bookmarkLink = bookmarkContainer.querySelector('.bookmark-icon');
        bookmarkLink.classList.toggle('bookmarked');

        fetch('bookmark/' + code, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken
            },
        }) 

        return;
    }


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