import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# I want to keep the header, and my injected propDynamicBody. I want to remove the old prop-title, prop-info-table, the old prop-body, prop-appendix, prop-signatures.
# The easiest way is to find <div id="proposalDoc" class="proposal-doc"> and replace everything until </section>
start_marker = '<div id="proposalDoc" class="proposal-doc">'
# find the start of proposalDoc
start_idx = html.find(start_marker)
# find the end of the section
end_idx = html.find('</section>', start_idx)

new_proposal_doc = """<div id="proposalDoc" class="proposal-doc" style="font-family: 'Times New Roman', serif; line-height: 1.5; font-size: 14px; position: relative;">
          <!-- Header (Bi-Logo) -->
          <div class="prop-header" style="display: flex; justify-content: space-between; align-items: start; border-bottom: 2px solid var(--color-primary); padding-bottom: 15px; margin-bottom: 25px;">
            <img src="ecolab-logo-tagline svg.svg" alt="Ecolab Logo" class="prop-logo" style="height: 60px;">
            <div style="text-align: right;">
                <img id="propCustomerLogo" src="" alt="Customer Logo" style="max-height: 60px; display: none;">
            </div>
          </div>

          <!-- Content Body (Fully Dynamic from DOCX) -->
          <div class="prop-body" id="propDynamicBody" style="outline: none;">
            <!-- Injected via JS -->
          </div>
        </div>
      """

new_html = html[:start_idx] + new_proposal_doc + html[end_idx:]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("HTML Fixed.")
