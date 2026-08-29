using System;
using System.Collections.Concurrent;
using System.Linq;
using System.Threading.Tasks;
using Xunit;

namespace AetherFi.SDSD.Tests
{
    public class Ledger
    {
        private readonly ConcurrentDictionary<string, decimal> _accounts = new();
        private readonly object _lock = new();

        public void SetBalance(string account, decimal amount) => _accounts[account] = amount;

        public decimal GetTotalBalance() => _accounts.Values.Sum();

        public bool Transfer(string from, string to, decimal amount)
        {
            lock (_lock)
            {
                if (!_accounts.TryGetValue(from, out var fromBal) || fromBal < amount) return false;
                _accounts[from] = fromBal - amount;
                _accounts[to] = _accounts.GetValueOrDefault(to, 0) + amount;
                return true;
            }
        }
    }

    public class TransferLedgerTests
    {
        [Fact]
        public async Task TestConservationOfMassConcurrent()
        {
            var ledger = new Ledger();
            ledger.SetBalance("ACC_A", 1000.00m);
            ledger.SetBalance("ACC_B", 1000.00m);
            var initialTotal = ledger.GetTotalBalance();

            var tasks = Enumerable.Range(0, 50).SelectMany(_ => new[]
            {
                Task.Run(() => ledger.Transfer("ACC_A", "ACC_B", 10.00m)),
                Task.Run(() => ledger.Transfer("ACC_B", "ACC_A", 5.00m))
            });

            await Task.WhenAll(tasks);

            Assert.Equal(initialTotal, ledger.GetTotalBalance());
        }
    }
}
