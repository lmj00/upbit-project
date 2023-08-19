const accountSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/sml_trade/account/'
);


function sendAccountSignal() {
    accountSocket.send(JSON.stringify({
        'signal': true,
    }));
}

let acIntervalId;

accountSocket.onopen = function (event) {
    acIntervalId = setInterval(sendAccountSignal, 1000);
}


accountSocket.onclose = function (event) {
    clearInterval(acIntervalId);
}


accountSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if (data.type == 'sml_account_balance') {
        const acbValue = data.value;
        const tradeValueElements = document.querySelectorAll('.TradeValue');

        tradeValueElements[0].textContent = acbValue.holding_krw;
        tradeValueElements[1].textContent = acbValue.total_assets;
        tradeValueElements[2].textContent = acbValue.total_purchase;
        tradeValueElements[3].textContent = acbValue.profit_or_loss;
        tradeValueElements[4].textContent = acbValue.total_evaluation;
        tradeValueElements[5].textContent = acbValue.rate_of_return;

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