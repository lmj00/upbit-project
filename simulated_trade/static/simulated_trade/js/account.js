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