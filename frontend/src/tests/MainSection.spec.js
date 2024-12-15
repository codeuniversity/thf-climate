import { mount } from '@vue/test-utils'
import { vi, describe, beforeEach, it, expect } from 'vitest'
import MainSection from '@/components/MainSection.vue'
import axios from 'axios'

vi.mock("axios")

vi.mock('plotly.js-dist-min', () => ({
  newPlot: vi.fn(),
  react: vi.fn(),
  update: vi.fn(),
}))

global.IntersectionObserver = vi.fn(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));

describe("MainSection.vue", () => {
  beforeEach(() => {
    vi.resetAllMocks()
  });

  it("renders the component properly", () => {
    const wrapper = mount(MainSection)
    expect(wrapper.exists()).toBe(true)
  })

  it("fetches NDVI data on mount", async () => {
    const wrapper = mount(MainSection)
  
    await wrapper.vm.$nextTick()
  
    expect(axios.get).toHaveBeenCalledWith(
      "https://thf-climate-run-1020174331409.europe-west3.run.app/index/ndvi",
      {
        params: {
          startDate: 1514761200, // 2018-01-01
          endDate: 1733007599,  // 2024-11-30
          location: "TEMPELHOFER_FELD",
          temporalResolution: "MONTHLY",
          aggregation: "MEAN",
        },
      }
    )
  })
  

  it("toggles the 'isExpanded' state", async () => {
    const wrapper = mount(MainSection)

    expect(wrapper.vm.isExpanded).toBe(false)

    await wrapper.vm.toggleExpand()

    expect(wrapper.vm.isExpanded).toBe(true)

    await wrapper.vm.toggleExpand()

    expect(wrapper.vm.isExpanded).toBe(false)
  })

  // add observer test
})
