bid_summary_prompt = """
Please generate a concise summary of the uploaded Request for Proposal (RFP) document. The summary should be structured with specific headings and content as follows:

Overview:

Title of the RFP: Include the title of the RFP.
Issuing Organization: Specify the name of the organization that issued the RFP.
Scope of Work:

Provide a clear and brief outline of the work that needs to be done as described in the RFP. Highlight any major project deliverables and the overall objectives.
Proposal Requirements:

Detail the guidelines for submitting the proposal. Include any specific instructions, formats, or mandatory elements that proposers must follow.
Mention any mandatory meetings (e.g., pre-proposal meetings) that the proposers need to attend.
Proposal Evaluation Criteria:

Outline the criteria that will be used to evaluate the proposals. Highlight the key factors that will influence the selection process, such as price, technical expertise, project timeline, and past performance.
Required Documentation:

List all documents that proposers must include with their proposal. This may include but is not limited to certifications, proof of qualifications, project plans, and financial statements.
Important Dates:

Provide a list of all critical dates related to the RFP process, including:
Proposal Release Date: The date the RFP was made available.
Mandatory Pre-Proposal Meeting Date: The scheduled date for any compulsory informational meetings.
Proposal Deadline: The cutoff date by which all proposals must be submitted.
Interview and Selection Date: When interviews (if any) will be conducted and the date by which the successful bidder will be selected.
Contract Start Date: The expected date on which work will commence according to the RFP.
Please ensure the summary is accurate, concise, and easy to understand, adhering to the structure and content requirements specified above.

"""