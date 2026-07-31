# evidence


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_2f63c1f44860", "created_at": "2026-07-30T03:05:55+00:00", "title": "Evidence"}
-->
# Evidence — exact decision-theory

Discrete problem: S={healthy,diseased}, A={no-biopsy,watch,biopsy}, informative test X∈{0,1,2}, Ŷ=f(X)=1 iff X==2, Z=Ŷ (coarse explanation).
R_V=Σ_v p(v)max_a Σ_s p(s|v)u(a,s); p(s|v)∝p(v|s)p(s).
- R_∅=−0.16, R_X=−0.008, R_{X,Ŷ,Z}=−0.008, R_Z=−0.0275.
- **C0** TVE=R_X−R_∅=**0.152**>0.
- **C3** R_{X∪Ŷ∪Z}=R_{X∪Ŷ}=−0.008 (Prop1, machine precision — Z=E(X,Ŷ) is a garbling); R_{X∪Ŷ}=R_X (Cor1, Ŷ redundant).
- **C1** R_{X∪x_H}−R_{x_H}=**0.057** (AI features add value over human's coarser signal).
- **C4** Δ_ind(R_Z−R_∅)=0.133 < TVE; Δ_cont(R_X−R_Z)=0.020>0 (explanation alone less valuable than full features).
- **C5** states=2, actions=3, prior sums to 1, R_∅=max_a E[u].
