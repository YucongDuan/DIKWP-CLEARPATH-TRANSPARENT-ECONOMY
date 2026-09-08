------------------------------ MODULE TOEP ------------------------------
EXTENDS Naturals, Sequences

CONSTANTS Routes
VARIABLES state, reasons, appealOpen, corrected, externalAuthority, worthScore

States == {"DRAFT", "EVIDENCED", "ANALYZED", "GO", "TEST", "PIVOT", "CLOSED", "CORRECTED"}

Init == /\ state = "DRAFT"
        /\ reasons = <<>>
        /\ appealOpen = FALSE
        /\ corrected = FALSE
        /\ externalAuthority = 0
        /\ worthScore = "NULL"

Evidence == /\ state = "DRAFT"
            /\ state' = "EVIDENCED"
            /\ UNCHANGED <<reasons, appealOpen, corrected, externalAuthority, worthScore>>

Analyze == /\ state = "EVIDENCED"
           /\ state' = "ANALYZED"
           /\ UNCHANGED <<reasons, appealOpen, corrected, externalAuthority, worthScore>>

Decide(s) == /\ state = "ANALYZED"
             /\ s \in {"GO", "TEST", "PIVOT", "CLOSED"}
             /\ state' = s
             /\ reasons' = IF s = "CLOSED" THEN Append(reasons, "NAMED_REASON") ELSE reasons
             /\ UNCHANGED <<appealOpen, corrected, externalAuthority, worthScore>>

Appeal == /\ state \in {"GO", "TEST", "PIVOT", "CLOSED"}
          /\ appealOpen' = TRUE
          /\ UNCHANGED <<state, reasons, corrected, externalAuthority, worthScore>>

Correct == /\ appealOpen
           /\ corrected' = TRUE
           /\ appealOpen' = FALSE
           /\ state' = "CORRECTED"
           /\ UNCHANGED <<reasons, externalAuthority, worthScore>>

Next == Evidence \/ Analyze \/ (\E s \in States : Decide(s)) \/ Appeal \/ Correct

NoExternalAuthority == externalAuthority = 0
NoWorthScore == worthScore = "NULL"
ClosedHasReason == state = "CLOSED" => Len(reasons) > 0
CorrectionRequiresAppeal == state = "CORRECTED" => corrected

=============================================================================
