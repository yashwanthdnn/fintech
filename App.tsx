import React, { useState } from 'react';
import { FinProvider, useFin } from './context/FinContext';
import { DemoBanner } from './components/layout/DemoBanner';
import { Navbar } from './components/layout/Navbar';
import { Sidebar } from './components/layout/Sidebar';
import { BottomNav } from './components/layout/BottomNav';
import { DashboardOverview } from './components/dashboard/DashboardOverview';
import { WalletSection } from './components/wallet/WalletSection';
import { GoalsSection } from './components/goals/GoalsSection';
import { LoanSimulatorSection } from './components/loan/LoanSimulatorSection';
import { InvestmentSimulatorSection } from './components/investment/InvestmentSimulatorSection';
import { HealthScoreSection } from './components/health/HealthScoreSection';
import { ProfileSection } from './components/profile/ProfileSection';
import { OnboardingModal } from './components/onboarding/OnboardingModal';
import { DepositModal } from './components/wallet/DepositModal';
import { SendMoneyModal } from './components/wallet/SendMoneyModal';
import { ReceiptModal } from './components/wallet/ReceiptModal';

const AppContent: React.FC = () => {
  const { activeSection, activeReceipt, setActiveReceipt } = useFin();

  // Global Modal States
  const [isDepositOpen, setIsDepositOpen] = useState(false);
  const [isSendOpen, setIsSendOpen] = useState(false);
  const [isOnboardingOpen, setIsOnboardingOpen] = useState(false);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col text-slate-900 selection:bg-emerald-100 selection:text-emerald-950 font-sans">
      {/* 1. Top Global Demo Banner */}
      <DemoBanner />

      {/* 2. Sticky Navbar */}
      <Navbar
        onOpenDeposit={() => setIsDepositOpen(true)}
        onOpenSend={() => setIsSendOpen(true)}
        onOpenOnboarding={() => setIsOnboardingOpen(true)}
      />

      {/* 3. Main Layout Container: Sidebar + Active Section Content */}
      <div className="flex-1 flex max-w-7xl w-full mx-auto">
        {/* Desktop Navigation Sidebar */}
        <Sidebar onOpenOnboarding={() => setIsOnboardingOpen(true)} />

        {/* Main Content Workspace */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8 pb-24 lg:pb-8 overflow-y-auto min-w-0">
          {activeSection === 'dashboard' && (
            <DashboardOverview
              onOpenDeposit={() => setIsDepositOpen(true)}
              onOpenSend={() => setIsSendOpen(true)}
            />
          )}

          {activeSection === 'wallet' && (
            <WalletSection
              isDepositOpen={isDepositOpen}
              setIsDepositOpen={setIsDepositOpen}
              isSendOpen={isSendOpen}
              setIsSendOpen={setIsSendOpen}
            />
          )}

          {activeSection === 'goals' && <GoalsSection />}

          {activeSection === 'loan' && <LoanSimulatorSection />}

          {activeSection === 'investment' && <InvestmentSimulatorSection />}

          {activeSection === 'health' && <HealthScoreSection />}

          {activeSection === 'profile' && <ProfileSection />}
        </main>
      </div>

      {/* 4. Mobile Bottom Navigation */}
      <BottomNav />

      {/* 5. Global Modals */}
      <DepositModal
        isOpen={isDepositOpen}
        onClose={() => setIsDepositOpen(false)}
      />

      <SendMoneyModal
        isOpen={isSendOpen}
        onClose={() => setIsSendOpen(false)}
      />

      <ReceiptModal
        isOpen={Boolean(activeReceipt)}
        transaction={activeReceipt}
        onClose={() => setActiveReceipt(null)}
      />

      <OnboardingModal
        isOpen={isOnboardingOpen}
        onClose={() => setIsOnboardingOpen(false)}
      />
    </div>
  );
};

export default function App() {
  return (
    <FinProvider>
      <AppContent />
    </FinProvider>
  );
}
