content = open('/Users/nguyenphong/Desktop/Inst.sale/index.html', encoding='utf-8').read()

new_home = """      <!-- SECTION 0: HOME / DASHBOARD (Ecolab-style) -->
      <section id="home" class="tab-content active -mx-4 -mt-8">

        <!-- == CHEVRON PANELS == -->
        <div class="flex flex-col md:flex-row" style="min-height: 340px;">

          <!-- Panel 1: Quotation -->
          <div class="home-panel group relative flex-1 cursor-pointer overflow-hidden"
            style="background: url('assets/hero_bg.png') center/cover no-repeat;"
            onclick="document.querySelector('[data-tab=\\'quotation\\']').click()">
            <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent group-hover:from-black/80 transition-all"></div>
            <div class="home-panel-chevron"></div>
            <div class="relative z-10 flex flex-col justify-end h-full p-7 text-white">
              <div class="size-12 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center mb-4 group-hover:bg-white/30 transition-colors">
                <span class="material-symbols-outlined text-2xl">request_quote</span>
              </div>
              <p class="font-bold text-lg leading-tight mb-1" data-i18n="tab_quote">Quotation</p>
              <p class="text-xs text-white/75 font-normal" data-i18n="home_quote_desc">Build professional price tables for any customer.</p>
              <div class="mt-4 flex items-center gap-1 text-xs font-bold text-white/90 group-hover:gap-2 transition-all">
                M\u1edf c\u00f4ng c\u1ee5 <span class="material-symbols-outlined text-sm">add</span>
              </div>
            </div>
          </div>

          <!-- Panel 2: Catsheets -->
          <div class="home-panel group relative flex-1 cursor-pointer overflow-hidden" style="background: #003DA5;"
            onclick="document.querySelector('[data-tab=\\'catsheets\\']').click()">
            <div class="absolute inset-0" style="background-image: radial-gradient(circle, rgba(255,255,255,0.08) 1px, transparent 1px); background-size: 22px 22px;"></div>
            <div class="home-panel-chevron"></div>
            <div class="relative z-10 flex flex-col justify-end h-full p-7 text-white">
              <div class="size-12 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center mb-4 group-hover:bg-white/30 transition-colors">
                <span class="material-symbols-outlined text-2xl">library_books</span>
              </div>
              <p class="font-bold text-lg leading-tight mb-1" data-i18n="tab_catsheets">T\u00e0i li\u1ec7u KT</p>
              <p class="text-xs text-white/75 font-normal" data-i18n="home_cat_desc">Access technical catsheets and marketing materials instantly.</p>
              <div class="mt-4 flex items-center gap-1 text-xs font-bold text-white/90 group-hover:gap-2 transition-all">
                M\u1edf c\u00f4ng c\u1ee5 <span class="material-symbols-outlined text-sm">add</span>
              </div>
            </div>
          </div>

          <!-- Panel 3: Proposal -->
          <div class="home-panel group relative flex-1 cursor-pointer overflow-hidden"
            style="background: linear-gradient(135deg, #1e3a5f 0%, #0f2540 100%);"
            onclick="document.querySelector('[data-tab=\\'proposal\\']').click()">
            <div class="relative z-10 flex flex-col justify-end h-full p-7 text-white">
              <div class="size-12 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center mb-4 group-hover:bg-white/30 transition-colors">
                <span class="material-symbols-outlined text-2xl">description</span>
              </div>
              <p class="font-bold text-lg leading-tight mb-1" data-i18n="tab_proposal">Proposal Maker</p>
              <p class="text-xs text-white/75 font-normal" data-i18n="home_prop_desc">Generate full partnership proposals in minutes.</p>
              <div class="mt-4 flex items-center gap-1 text-xs font-bold text-white/90 group-hover:gap-2 transition-all">
                M\u1edf c\u00f4ng c\u1ee5 <span class="material-symbols-outlined text-sm">add</span>
              </div>
            </div>
          </div>

        </div>

        <!-- == STATS BAR == -->
        <div class="bg-[#003DA5] py-10">
          <div class="max-w-7xl mx-auto px-8 flex flex-col md:flex-row items-start md:items-center gap-8 md:gap-0 md:justify-between">
            <div class="md:w-2/5">
              <h3 class="text-white font-bold text-2xl md:text-3xl leading-snug mb-2">Be Bold \u2014 Be Faster</h3>
              <div class="w-12 h-1 bg-white/40 rounded mt-3"></div>
            </div>
            <div class="md:w-3/5 grid grid-cols-2 md:grid-cols-3 gap-8">
              <div class="text-white">
                <p class="text-4xl font-black tabular-nums">300<span class="text-2xl">+</span></p>
                <p class="text-xs font-bold uppercase tracking-widest text-white/60 mt-1">S\u1ea3n ph\u1ea9m Ecolab</p>
              </div>
              <div class="text-white">
                <p class="text-4xl font-black tabular-nums">500<span class="text-2xl">+</span></p>
                <p class="text-xs font-bold uppercase tracking-widest text-white/60 mt-1">T\u00e0i li\u1ec7u k\u1ef9 thu\u1eadt</p>
              </div>
              <div class="text-white">
                <p class="text-4xl font-black tabular-nums">4</p>
                <p class="text-xs font-bold uppercase tracking-widest text-white/60 mt-1">B\u1ed9 c\u00f4ng c\u1ee5 t\u00edch h\u1ee3p</p>
              </div>
            </div>
          </div>
        </div>

        <!-- == SDS QUICK LINK == -->
        <div class="bg-white py-10 border-b border-slate-100">
          <div class="max-w-7xl mx-auto px-8 flex flex-col md:flex-row items-center gap-8">
            <div class="flex-1">
              <h3 class="text-xl font-bold text-[#003DA5] mb-2">Tra c\u1ee9u SDS nhanh</h3>
              <p class="text-sm text-slate-500 font-medium">Truy c\u1eadp b\u1ea3ng d\u1eef li\u1ec7u an to\u00e0n ngay l\u1eadp t\u1ee9c cho m\u1ecdi s\u1ea3n ph\u1ea9m Ecolab t\u1ea1i Vi\u1ec7t Nam.</p>
            </div>
            <button onclick="document.querySelector('[data-tab=\\'sds\\']').click()"
              class="flex items-center gap-2 bg-[#003DA5] text-white font-bold px-6 py-3 rounded-full text-sm hover:bg-[#0056ac] transition-colors shadow-md whitespace-nowrap">
              <span class="material-symbols-outlined">gavel</span>
              M\u1edf SDS Viewer
            </button>
          </div>
        </div>

      </section>

"""

# Find the start of #home section
start_marker = '      <!-- SECTION 0: HOME / DASHBOARD (Ecolab-style) -->'
# Find the next section after home
end_marker = '<!-- SECTON 1: QUOTATION BUILDER -->'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

print(f"start_idx={start_idx}, end_idx={end_idx}")

if start_idx != -1 and end_idx != -1:
    # Find the actual indentation before end_marker
    line_start = content.rfind('\n', 0, end_idx) + 1
    new_content = content[:start_idx] + new_home + '      ' + content[line_start:]
    open('/Users/nguyenphong/Desktop/Inst.sale/index.html', 'w', encoding='utf-8').write(new_content)
    print(f"Done. File length: {len(new_content)}")
else:
    print("Markers not found!")
    print("Looking for end alternatives...")
    for marker in ['<!-- SECTON', '<!-- SECTION 1', 'QUOTATION BUILDER']:
        idx = content.find(marker)
        print(f"  '{marker}': {idx}")
