package com.aetherfi.sdsd;

import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import java.util.concurrent.*;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class TransferLedgerTest {

    static class Ledger {
        private final ConcurrentHashMap<String, BigDecimal> accounts = new ConcurrentHashMap<>();

        public void setBalance(String account, BigDecimal amount) {
            accounts.put(account, amount);
        }

        public BigDecimal getTotalBalance() {
            return accounts.values().stream().reduce(BigDecimal.ZERO, BigDecimal::add);
        }

        public synchronized boolean transfer(String from, String to, BigDecimal amount) {
            BigDecimal fromBalance = accounts.getOrDefault(from, BigDecimal.ZERO);
            if (fromBalance.compareTo(amount) < 0) return false;
            accounts.put(from, fromBalance.subtract(amount));
            accounts.put(to, accounts.getOrDefault(to, BigDecimal.ZERO).add(amount));
            return true;
        }
    }

    @Test
    public void testConservationOfMassConcurrent() throws InterruptedException {
        Ledger ledger = new Ledger();
        ledger.setBalance("ACC_A", new BigDecimal("1000.00"));
        ledger.setBalance("ACC_B", new BigDecimal("1000.00"));
        BigDecimal initialTotal = ledger.getTotalBalance();

        ExecutorService executor = Executors.newFixedThreadPool(10);
        for (int i = 0; i < 50; i++) {
            executor.submit(() -> ledger.transfer("ACC_A", "ACC_B", new BigDecimal("10.00")));
            executor.submit(() -> ledger.transfer("ACC_B", "ACC_A", new BigDecimal("5.00")));
        }
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);

        assertEquals(initialTotal, ledger.getTotalBalance(), "Conservation of mass violated!");
    }
}
