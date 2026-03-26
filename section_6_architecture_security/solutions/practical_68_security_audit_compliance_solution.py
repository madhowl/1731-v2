#!/usr/bin/env python3
"""
Практическое занятие 68: Аудит безопасности и соответствие требованиям
Решение упражнений
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


# ==============================================================================
# УПРАЖНЕНИЕ 1: Compliance Frameworks
# ==============================================================================

print("=" * 60)
print("Упражнение 1: Compliance Frameworks")
print("=" * 60)


class ComplianceFramework(Enum):
    GDPR = "GDPR"
    HIPAA = "HIPAA"
    PCI_DSS = "PCI-DSS"
    SOC2 = "SOC2"
    ISO_27001 = "ISO-27001"


@dataclass
class Control:
    id: str
    name: str
    description: str
    category: str
    mandatory: bool = True


class ComplianceManager:
    """Менеджер соответствия требованиям"""
    
    def __init__(self, framework: ComplianceFramework):
        self.framework = framework
        self.controls: List[Control] = []
        self.implemented_controls: List[str] = []
    
    def add_control(self, control: Control):
        self.controls.append(control)
    
    def mark_implemented(self, control_id: str):
        if control_id not in self.implemented_controls:
            self.implemented_controls.append(control_id)
    
    def get_compliance_score(self) -> float:
        if not self.controls:
            return 0.0
        
        implemented = sum(1 for c in self.controls if c.id in self.implemented_controls)
        mandatory = sum(1 for c in self.controls if c.mandatory)
        
        if mandatory == 0:
            return 0.0
        
        return (implemented / mandatory) * 100
    
    def get_gaps(self) -> List[Control]:
        return [c for c in self.controls if c.id not in self.implemented_controls and c.mandatory]


gdpr = ComplianceManager(ComplianceFramework.GDPR)

gdpr.add_control(Control("A.1", "Data Protection Policy", "Политика защиты данных", "Governance", True))
gdpr.add_control(Control("A.2", "Data Breach Notification", "Уведомление о утечке данных", "Response", True))
gdpr.add_control(Control("A.3", "Privacy by Design", "Конфиденциальность по умолчанию", "Design", True))
gdpr.add_control(Control("A.4", "Data Subject Rights", "Права субъекта данных", "Rights", True))

gdpr.mark_implemented("A.1")
gdpr.mark_implemented("A.2")

score = gdpr.get_compliance_score()
print(f"Framework: {gdpr.framework.value}")
print(f"Compliance score: {score:.1f}%")

gaps = gdpr.get_gaps()
print(f"Gaps found: {len(gaps)}")
for gap in gaps:
    print(f"  - {gap.id}: {gap.name}")


# ==============================================================================
# УПРАЖНЕНИЕ 2: Security Audit
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 2: Security Audit")
print("=" * 60)


class AuditStatus(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    NOT_APPLICABLE = "not_applicable"


@dataclass
class AuditFinding:
    control_id: str
    status: AuditStatus
    evidence: str
    notes: str = ""


class SecurityAudit:
    """Аудит безопасности"""
    
    def __init__(self, audit_name: str):
        self.audit_name = audit_name
        self.findings: List[AuditFinding] = []
        self.audit_date = datetime.now()
    
    def add_finding(self, finding: AuditFinding):
        self.findings.append(finding)
    
    def get_summary(self) -> Dict[str, Any]:
        status_counts = {}
        for finding in self.findings:
            status = finding.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            'audit_name': self.audit_name,
            'date': self.audit_date.isoformat(),
            'total_findings': len(self.findings),
            'by_status': status_counts,
            'pass_rate': (status_counts.get('pass', 0) / len(self.findings) * 100) if self.findings else 0
        }


audit = SecurityAudit("Annual Security Audit 2024")

audit.add_finding(AuditFinding(
    control_id="A.1",
    status=AuditStatus.PASS,
    evidence="Policy document dated 2024-01-15",
    notes="All required sections present"
))

audit.add_finding(AuditFinding(
    control_id="A.2",
    status=AuditStatus.WARNING,
    evidence="Procedure exists but not tested",
    notes="Recommend conducting a drill"
))

audit.add_finding(AuditFinding(
    control_id="A.3",
    status=AuditStatus.FAIL,
    evidence="No documentation found",
    notes="Needs immediate attention"
))

summary = audit.get_summary()
print(f"Audit: {summary['audit_name']}")
print(f"Date: {summary['date']}")
print(f"Pass rate: {summary['pass_rate']:.1f}%")


# ==============================================================================
# УПРАЖНЕНИЕ 3: Policy Management
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 3: Policy Management")
print("=" * 60)


class PolicyStatus(Enum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


@dataclass
class Policy:
    id: str
    title: str
    category: str
    status: PolicyStatus
    version: str
    owner: str
    created_at: datetime
    last_reviewed: datetime = None


class PolicyManager:
    """Управление политиками"""
    
    def __init__(self):
        self.policies: List[Policy] = []
    
    def create_policy(self, title: str, category: str, owner: str) -> Policy:
        policy = Policy(
            id=f"POL-{len(self.policies) + 1:04d}",
            title=title,
            category=category,
            status=PolicyStatus.DRAFT,
            version="1.0",
            owner=owner,
            created_at=datetime.now()
        )
        self.policies.append(policy)
        return policy
    
    def update_status(self, policy_id: str, new_status: PolicyStatus) -> bool:
        for policy in self.policies:
            if policy.id == policy_id:
                policy.status = new_status
                return True
        return False
    
    def get_overdue_reviews(self, days: int = 90) -> List[Policy]:
        overdue = []
        threshold = datetime.now() - timedelta(days=days)
        
        for policy in self.policies:
            if policy.last_reviewed and policy.last_reviewed < threshold:
                overdue.append(policy)
        
        return overdue
    
    def get_policies_by_status(self, status: PolicyStatus) -> List[Policy]:
        return [p for p in self.policies if p.status == status]


from datetime import timedelta

policy_manager = PolicyManager()

p1 = policy_manager.create_policy("Information Security Policy", "Security", "CISO")
p2 = policy_manager.create_policy("Data Classification Policy", "Data", "DPO")
p3 = policy_manager.create_policy("Acceptable Use Policy", "Usage", "IT Manager")

policy_manager.update_status(p1.id, PolicyStatus.APPROVED)
policy_manager.update_status(p2.id, PolicyStatus.PUBLISHED)

published = policy_manager.get_policies_by_status(PolicyStatus.PUBLISHED)
print(f"Published policies: {len(published)}")
for policy in published:
    print(f"  - {policy.title} ({policy.id})")


# ==============================================================================
# УПРАЖНЕНИЕ 4: Risk Assessment
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: Risk Assessment")
print("=" * 60)


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Risk:
    id: str
    name: str
    description: str
    likelihood: int
    impact: int
    level: RiskLevel = RiskLevel.LOW
    
    def __post_init__(self):
        self.calculate_level()
    
    def calculate_level(self):
        score = self.likelihood * self.impact
        
        if score >= 15:
            self.level = RiskLevel.CRITICAL
        elif score >= 10:
            self.level = RiskLevel.HIGH
        elif score >= 5:
            self.level = RiskLevel.MEDIUM
        else:
            self.level = RiskLevel.LOW


class RiskRegister:
    """Реестр рисков"""
    
    def __init__(self):
        self.risks: List[Risk] = []
        self._next_id = 1
    
    def add_risk(self, name: str, description: str, likelihood: int, impact: int) -> Risk:
        risk = Risk(
            id=f"RISK-{self._next_id:04d}",
            name=name,
            description=description,
            likelihood=likelihood,
            impact=impact
        )
        self._next_id += 1
        self.risks.append(risk)
        return risk
    
    def get_by_level(self, level: RiskLevel) -> List[Risk]:
        return [r for r in self.risks if r.level == level]
    
    def get_summary(self) -> Dict[str, Any]:
        return {
            'total': len(self.risks),
            'by_level': {
                'critical': len(self.get_by_level(RiskLevel.CRITICAL)),
                'high': len(self.get_by_level(RiskLevel.HIGH)),
                'medium': len(self.get_by_level(RiskLevel.MEDIUM)),
                'low': len(self.get_by_level(RiskLevel.LOW))
            }
        }


register = RiskRegister()

register.add_risk("Data Breach", "Unauthorized access to sensitive data", 4, 5)
register.add_risk("Ransomware", "Malicious encryption of data", 3, 5)
register.add_risk("Insider Threat", "Malicious actions by employees", 2, 4)
register.add_risk("DDoS Attack", "Service unavailability", 3, 3)

summary = register.get_summary()
print("Risk Summary:")
print(f"  Total risks: {summary['total']}")
for level, count in summary['by_level'].items():
    print(f"  {level.upper()}: {count}")


# ==============================================================================
# УПРАЖНЕНИЕ 5: Audit Report
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 5: Audit Report")
print("=" * 60)


class AuditReport:
    """Генератор отчёта об аудите"""
    
    def __init__(self, audit: SecurityAudit):
        self.audit = audit
        self.sections: List[str] = []
    
    def add_section(self, title: str, content: str):
        self.sections.append(f"## {title}\n\n{content}")
    
    def generate_markdown(self) -> str:
        lines = [
            f"# {self.audit.audit_name}",
            f"**Date:** {self.audit.audit_date.strftime('%Y-%m-%d')}",
            "",
            "---",
            ""
        ]
        
        lines.extend(self.sections)
        
        summary = self.audit.get_summary()
        lines.extend([
            "",
            "---",
            "",
            "## Summary",
            "",
            f"- **Total Findings:** {summary['total_findings']}",
            f"- **Pass Rate:** {summary['pass_rate']:.1f}%",
            ""
        ])
        
        return "\n".join(lines)
    
    def generate_json(self) -> Dict[str, Any]:
        summary = self.audit.get_summary()
        
        return {
            'audit': {
                'name': self.audit.audit_name,
                'date': self.audit.audit_date.isoformat(),
                'findings': [
                    {
                        'control_id': f.control_id,
                        'status': f.status.value,
                        'evidence': f.evidence,
                        'notes': f.notes
                    }
                    for f in self.audit.findings
                ],
                'summary': summary
            }
        }


report = AuditReport(audit)
report.add_section("Introduction", "This is an annual security audit report.")
report.add_section("Methodology", "The audit was conducted using ISO 27001 framework.")

print("Generated Report (Markdown):")
print(report.generate_markdown()[:500])


print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)
