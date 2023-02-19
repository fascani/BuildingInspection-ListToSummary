# BuildingInspection-ListToSummary

Streamlit app that takes in a list of comments from a building inspector and returns a professional summary of it. For instance, if the input is

* Bedroom 1
* Walls lining paper and poor
* Floor is tiled and good
* Ceiling and some walls lining paper and good
* Damp stain to ceiling
* Windows are PVCu double glazed, we tested one, seem good
* One glazed pane was cracked
* Floor is carpet and poor

The return should be:

"Upon inspection of Bedroom 1, the walls were observed to be lined with paper, and it was determined that they are in poor condition. The floor is tiled and appeared to be in good condition. The ceiling and some of the walls are also lined with paper, which appears to be in good condition. However, a damp stain was noted on the ceiling, which requires further investigation to determine the cause and extent of the issue. The windows are PVCu double-glazed, and one window was tested and appears to be in good condition. However, it should be noted that one glazed pane was found to be cracked, which may require replacement. The floor is covered in carpet, which is in poor condition and may require replacement. Overall, some remedial works may be necessary to address the issues identified in Bedroom 1, including investigating the damp stain, replacing the damaged glazed pane, and improving the condition of the walls and flooring"
