## Tags

Reporting

DAVE nodes are generic building block. This is nice because it allows you to build anything you want.

But then you need a report.

Reports are intended to be read by humans. So it makes sense to view the model from a certain perspective, for example a mooring analysis perspective or a lift-analysis perspective.
The perspective from which you look at the model determines what is important and what is not.

Problem is: DAVE has no idea what kind of thing you modelled. And it may even be a mix of things. Maybe you
have modelled a vessel that is performing a lift while moored. The cable nodes that are used for mooring lines should be reported in the "mooring" sections of the report while the cable nodes
that are used to model slings should instead be reported in the "rigging section".

The reporting section of DAVE needs to know what is what, and the only way for DAVE to know it is if we tell it. So we need to
tell the reporing section which nodes should be included in the mooring report and which nodes should be included in the
rigging section.

Enter TAGS

Tags offer a way to "tag" nodes with one or more tags (labels). 