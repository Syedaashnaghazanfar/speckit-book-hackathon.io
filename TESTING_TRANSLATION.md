# Testing the Translation System

## Quick Start Testing Guide

Follow these steps to test the English-Urdu translation functionality:

## Prerequisites

1. **Backend Running**
   ```bash
   cd backend
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Verify backend is running:
   ```bash
   curl http://localhost:8000/api/translate/health
   ```

   Expected response:
   ```json
   {
     "status": "healthy",
     "service": "translation",
     "supported_languages": ["en", "ur"],
     "provider": "gemini-2.5-flash"
   }
   ```

2. **Frontend Running**
   ```bash
   cd frontend/my-website
   npm start
   ```

   Opens: http://localhost:3000

## Test Cases

### Test 1: Homepage Translation

**Steps:**
1. Navigate to http://localhost:3000
2. Click the language toggle button (🌐 icon in navbar)
3. Observe translation progress bar at top
4. Wait for translation to complete

**Expected Results:**
- ✓ Progress bar appears showing "Translating... X / Y"
- ✓ Hero title translates to Urdu
- ✓ Hero subtitle translates to Urdu
- ✓ Feature cards translate to Urdu
- ✓ Buttons translate to Urdu
- ✓ Layout switches to RTL (text aligned right)
- ✓ Technical terms like "ROS 2", "SLAM", "Gazebo" remain in English
- ✓ Progress bar disappears when complete

### Test 2: Documentation Page Translation

**Steps:**
1. Navigate to: http://localhost:3000/docs/Module-1-ROS2/week-01-intro-physical-ai
2. Click language toggle button
3. Observe translation

**Expected Results:**
- ✓ Page title translates
- ✓ Headings (h1, h2, h3) translate
- ✓ Paragraph text translates
- ✓ List items translate
- ✓ Code blocks remain in English (LTR)
- ✓ Technical terms preserved:
  - "Physical AI"
  - "ROS 2"
  - "SLAM"
  - "LIDAR"
  - "Python"
  - "API"
- ✓ Mermaid diagrams not affected
- ✓ RTL layout applied

### Test 3: Navigation Translation

**Steps:**
1. On any page, click language toggle
2. Observe sidebar navigation

**Expected Results:**
- ✓ Sidebar menu items translate
- ✓ "Course Modules" translates
- ✓ Module names translate
- ✓ Week titles translate
- ✓ Navigation remains functional
- ✓ RTL layout applied to sidebar

### Test 4: Technical Term Preservation

**Steps:**
1. Navigate to a technical page
2. Toggle to Urdu
3. Inspect these terms

**Expected to Remain in English:**
```
ROS 2, Gazebo, Isaac Sim, Python, SLAM, LIDAR,
API, JSON, GPU, NVIDIA, Docker, GitHub, URDF,
VLA, LLM, Transformer, CUDA, Ubuntu, Linux
```

**Expected Results:**
- ✓ All technical terms remain in English
- ✓ Terms are embedded correctly in Urdu sentences
- ✓ No translation of code syntax
- ✓ URLs remain unchanged

### Test 5: Code Block Preservation

**Steps:**
1. Navigate to page with code examples
2. Toggle to Urdu
3. Inspect code blocks

**Expected Results:**
- ✓ Code remains in English
- ✓ Code remains LTR (left-to-right)
- ✓ Syntax highlighting preserved
- ✓ Code comments not translated
- ✓ Code indentation preserved

### Test 6: Revert to English

**Steps:**
1. While on Urdu mode
2. Click language toggle again
3. Observe reversion

**Expected Results:**
- ✓ All content reverts to original English
- ✓ Layout switches back to LTR
- ✓ No visual artifacts
- ✓ Navigation works correctly
- ✓ Fast reversion (no API calls)

### Test 7: Translation Cache

**Steps:**
1. Toggle to Urdu (first time)
2. Note translation time
3. Toggle back to English
4. Toggle to Urdu again (second time)
5. Note translation time

**Expected Results:**
- ✓ Second translation is faster
- ✓ Cached translations used
- ✓ No duplicate API calls
- ✓ Identical translations

### Test 8: Error Handling

**Steps:**
1. Stop the backend server
2. Toggle to Urdu
3. Observe error handling

**Expected Results:**
- ✓ Error message appears
- ✓ "Translation failed" message shown
- ✓ "Retry" button appears
- ✓ Original content remains visible
- ✓ Layout doesn't break

**Then:**
4. Start backend server
5. Click "Retry" button

**Expected Results:**
- ✓ Translation resumes
- ✓ Progress bar appears
- ✓ Translation completes successfully

### Test 9: Mobile Responsive

**Steps:**
1. Open DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select mobile device (iPhone, Android)
4. Toggle to Urdu

**Expected Results:**
- ✓ Language toggle button visible
- ✓ Progress bar responsive
- ✓ Content translates correctly
- ✓ RTL layout works on mobile
- ✓ No horizontal scroll
- ✓ Touch interactions work

### Test 10: Persistence

**Steps:**
1. Toggle to Urdu
2. Wait for translation
3. Refresh page (F5)

**Expected Results:**
- ✓ Page loads in Urdu
- ✓ RTL layout applied immediately
- ✓ Content translates on load
- ✓ Language preference persisted

**Then:**
4. Toggle to English
5. Close tab
6. Reopen website

**Expected Results:**
- ✓ Page loads in English
- ✓ English preference persisted

## Visual Verification

### RTL Layout Check

When in Urdu mode, verify:
- [ ] Text aligned to the right
- [ ] Navbar items reversed
- [ ] Sidebar on the left side (opposite)
- [ ] Breadcrumbs flow right-to-left
- [ ] Pagination arrows flipped
- [ ] Search box aligned right
- [ ] Footer content aligned right

### Urdu Font Rendering

Check that Urdu text uses proper font:
- [ ] Nastaliq style font for Urdu
- [ ] Proper ligatures and joining
- [ ] No broken characters
- [ ] Readable font size
- [ ] Proper line height

## Browser Compatibility

Test in these browsers:

1. **Chrome/Edge (Chromium)**
   - [ ] Translation works
   - [ ] RTL layout correct
   - [ ] Urdu fonts render

2. **Firefox**
   - [ ] Translation works
   - [ ] RTL layout correct
   - [ ] Urdu fonts render

3. **Safari** (if available)
   - [ ] Translation works
   - [ ] RTL layout correct
   - [ ] Urdu fonts render

## Performance Testing

### Translation Speed

Measure translation time:

1. **Small Page** (Homepage)
   - Expected: < 2 seconds
   - Elements: ~50

2. **Medium Page** (Intro doc)
   - Expected: < 5 seconds
   - Elements: ~100-150

3. **Large Page** (Full module)
   - Expected: < 10 seconds
   - Elements: ~200-300

### Network Inspection

1. Open DevTools → Network tab
2. Toggle to Urdu
3. Observe API calls

**Expected:**
- ✓ Batch translation calls (not individual)
- ✓ 1-3 requests for typical page
- ✓ Request payload ~50 items per batch
- ✓ Response time < 3 seconds per batch

## Console Verification

Open browser console (F12) and check for:

1. **Info Messages**
   ```
   Language changed to: ur, RTL: true
   Translation request: en → ur, Text length: ...
   Translation completed: Cached=false, Confidence=...
   ```

2. **No Errors**
   - No red error messages
   - No warning about missing context
   - No network errors (unless testing error handling)

## Common Issues and Solutions

### Issue: Translation Not Starting

**Check:**
1. Backend running? `curl http://localhost:8000/api/translate/health`
2. Console errors?
3. Network tab shows requests?

**Solution:**
- Restart backend
- Clear browser cache
- Check CORS settings

### Issue: Partial Translation

**Check:**
1. Some elements not translating?
2. Check if element has `data-no-translate`
3. Check if element is in `NON_TRANSLATABLE_SELECTORS`

**Solution:**
- Review `translationUtils.ts`
- Add element selector to `TRANSLATABLE_SELECTORS`

### Issue: Technical Terms Translating

**Check:**
1. Which terms are translating?
2. Check spelling/capitalization

**Solution:**
- Add term to `TECHNICAL_TERMS` in `translationUtils.ts`
- Rebuild and test

### Issue: RTL Layout Issues

**Check:**
1. `html[dir="rtl"]` applied?
2. `.rtl` class on root?
3. CSS rules in `custom.css`?

**Solution:**
- Check `LanguageContext.tsx` applies dir attribute
- Review RTL CSS rules
- Check for conflicting styles

### Issue: Slow Translation

**Check:**
1. How many elements?
2. Cache working?
3. Batch size?

**Solution:**
- Reduce batch size in `useContentTranslation.ts`
- Check cache statistics
- Use `console.log` to debug

## Success Criteria

All tests pass when:

- [x] Homepage translates completely
- [x] Documentation pages translate
- [x] Navigation translates
- [x] Technical terms preserved
- [x] Code blocks remain LTR
- [x] RTL layout applied correctly
- [x] Revert to English works
- [x] Cache improves performance
- [x] Error handling works
- [x] Mobile responsive
- [x] Language preference persists
- [x] No console errors
- [x] Performance acceptable

## Reporting Issues

If you find issues, provide:

1. **Steps to reproduce**
2. **Expected behavior**
3. **Actual behavior**
4. **Browser and version**
5. **Console errors** (screenshot)
6. **Network tab** (screenshot)

## Next Steps

After successful testing:

1. Document any issues found
2. Test with real users
3. Gather feedback on translation quality
4. Consider adding more languages
5. Optimize performance based on metrics

---

**Happy Testing!** 🚀

For questions or issues, refer to:
- `TRANSLATION_SYSTEM.md` for architecture details
- `frontend/my-website/src/utils/translationUtils.ts` for configuration
- Backend API docs at `http://localhost:8000/docs`
