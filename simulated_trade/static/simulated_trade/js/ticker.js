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
                abookmark.textContent = '★';
                abookmark.className = 'bookmark-icon';
                sbookmark.appendChild(abookmark);
                tdBookmark.appendChild(sbookmark);
                tr.appendChild(tdBookmark);

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

    }
}