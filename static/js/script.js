document.addEventListener('DOMContentLoaded', () => {
    const dashboardLink = document.getElementById('dashboard-link');
    const depositLink = document.getElementById('deposit-link');
    const transferLink = document.getElementById('transfer-link');
    const transactionsLink = document.getElementById('transactions-link');
    const mainContent = document.getElementById('main-content');
    const changePinLink = document.getElementById('change_pin');
    const logoutLink = document.getElementById('logout');
    const loginLink = document.getElementById('login');
    const transactionsContent = document.getElementById('transactions-content');

    function loadDashboard() {
        fetch('/dashboard', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            mainContent.innerHTML = `
                <div id="dashboard">
                    <h1>Dashboard</h1>
                    <div class="summary">
                        <div class="card">
                            <h2>Total Balance</h2>
                            <p>USD ${data.balance}</p>
                        </div>
                    </div>
                    <div class="statistics card">
                        <h2>Statistics</h2>
                        <div style="height: 200px; background: #e3e3e3; border-radius: 10px;">
                            <!-- Placeholder for the chart -->
                        </div>
                    </div>
                    <div class="goals card">
                        <h2>Goals</h2>
                        <p>Summer Vacation: 62% reached</p>
                    </div>
                    <div class="spending-overview card">
                        <h2>Spending Overview</h2>
                        <div style="height: 100px; background: #e3e3e3; border-radius: 10px;">
                            <!-- Placeholder for spending overview -->
                        </div>
                    </div>
                </div>
            `;
            transactionsContent.innerHTML = `
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Transaction Type</th>
                            <th>Amount</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.transactions.map(trans => `
                            <tr>
                                <td>${trans.transaction_type}</td>
                                <td style="color: ${trans.transaction_type === 'Withdrawal' ? 'red' : 'green'};">
                                    ${trans.transaction_type === 'Withdrawal' ? '-' : '+'}${trans.amount}
                                </td>
                                <td>${trans.timestamp}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        })
        .catch(error => {
            console.error('Error loading content:', error);
            mainContent.innerHTML = '<p>Error loading content. Please try again later.</p>';
            transactionsContent.innerHTML = '';
        });
    }

    function loadContent(url) {
        fetch(url)
            .then(response => response.text())
            .then(html => {
                mainContent.innerHTML = html;
                transactionsContent.innerHTML = ''; // Clear transactions content if not needed
            })
            .catch(error => {
                console.error('Error loading content:', error);
                mainContent.innerHTML = '<p>Error loading content. Please try again later.</p>';
                transactionsContent.innerHTML = '';
            });
    }

    dashboardLink.addEventListener('click', () => {
        loadDashboard();
        setActive(dashboardLink);
    });
    transferLink.addEventListener('click', () => {
        loadContent('transfer');
        setActive(transferLink);
    });
    transactionsLink.addEventListener('click', () => {
        loadContent('withdraw');
        setActive(transactionsLink);
    });
    depositLink.addEventListener('click', () => {
        loadContent('deposit');
        setActive(depositLink);
    });
    if (changePinLink) {
        changePinLink.addEventListener('click', () => {
            loadContent('change_pin');
            setActive(changePinLink);
        });
    }
    if (logoutLink) {
        logoutLink.addEventListener('click', () => {
            loadContent('logout');
            setActive(logoutLink);
        });
    }
    if (loginLink) {
        loginLink.addEventListener('click', () => {
            loadContent('login');
            setActive(loginLink);
        });
    }

    loadDashboard();
    setActive(dashboardLink);

    function setActive(element) {
        document.querySelectorAll('.menu-item').forEach(item => {
            item.classList.remove('active');
        });
        element.classList.add('active');
    }
});
