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

        tradeValueElements[0].textContent = acbValue.holding_krw.toLocaleString();
        tradeValueElements[1].textContent = acbValue.total_assets.toLocaleString();
        tradeValueElements[2].textContent = acbValue.total_purchase.toLocaleString();
        tradeValueElements[3].textContent = acbValue.profit_or_loss.toLocaleString();
        tradeValueElements[4].textContent = acbValue.total_evaluation.toLocaleString();
        tradeValueElements[5].textContent = acbValue.rate_of_return.toLocaleString();

    } else if (data.type == 'sml_account') {
        const coinTable = document.querySelector('.CoinTable');
        const coinHeaderRow = coinTable.querySelector('.CoinHeaderRow');

        const existingCoinRows = coinTable.querySelectorAll('.CoinRow');
        existingCoinRows.forEach(row => row.remove());

        data.value.forEach(coin => {
            const coinRow = document.createElement('div');
            coinRow.classList.add('CoinRow');

            coinRow.innerHTML = `
                <div class="CoinValue">${coin.name}</div>
                <div class="CoinValue">${coin.balance.toLocaleString()}</div>
                <div class="CoinValue">${coin.avg_buy_price.toLocaleString()}</div>
                <div class="CoinValue">${coin.amount_money.toLocaleString()}</div>
                <div class="CoinValue">${coin.valuation_amount.toLocaleString()}</div>
                <div class="CoinValue">${coin.rate_of_return.toLocaleString()}</div>
            `;

            coinHeaderRow.insertAdjacentElement('afterend', coinRow);
        });
    }
}