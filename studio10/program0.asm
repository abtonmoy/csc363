


LEFT CODE -> t0
RIGHT CODE -> t1

B(!CMPOP) t0, t1, label

THEN_EXPR CODE
J label

label:





LEFT CODE -> t0
RIGHT CODE -> t1

B(!CMPOP) t0, t1, else_label

then_label:
THEN_EXPR CODE
J done_label

else_label:
ELSE_EXPR CODE
J done_label

done_label:




while_label:
LEFT CODE -> t0
RIGHT CODE -> t1
B(!CMPOP) t0, t1, done_label

body_label:
BODY_EXPR CODE
J while_label



done_label: