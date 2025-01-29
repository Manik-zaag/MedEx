from behave import *
from icecream import ic

from pages.BrandDetailsPage import BrandDetailsPage
from pages.CompanyBrandsPage import CompanyBrandsPage
from pages.CompanyPage import CompanyPage


@given(u'I navigate to the MedEx Companies page')
def step_impl(context):
    context.company_page = CompanyPage(context.driver)
    context.company_page.navigate_to_base_page(context)
    assert context.company_page.display_status_of_company_page()


@when(u'I click on each company name')
def step_impl(context):
    context.company_page.handle_pagination()
    ic(len(context.company_page.company_links))
    # ic(context.company_page.company_links)


@when(u'I view all brands if available')
def step_impl(context):
    context.company_brands_page = CompanyBrandsPage(context.driver)
    total_links = len(context.company_page.company_links)
    for index, company_link in enumerate(context.company_page.company_links, start=1):
        context.driver.get(company_link)
        assert context.company_brands_page.retrieve_current_url().__eq__(company_link)
        # ic("--------------", company_link, "--------------")
        context.company_brands_page.handle_pagination()
        ic(len(context.company_brands_page.brand_links))

        # Print the traversed company link count
        ic(f"Completed Company links: {index} out of {total_links}")

    # context.company_brands_page = CompanyBrandsPage(context.driver)
    # context.driver.get("https://medex.com.bd/companies/127/everest-pharmaceuticals-ltd")
    # # context.driver.get("https://medex.com.bd/companies/304/alien-pharma/brands")
    # # context.driver.get("https://medex.com.bd/companies/2/aci-limited")
    # # context.driver.get("https://medex.com.bd/companies/466/shinil-pharma-limited/brands")
    # context.company_brands_page.handle_pagination()
    # ic(len(context.company_brands_page.brand_links))
    # ic(context.company_brands_page.brand_links)


@when(u'I click on each brand')
def step_impl(context):
    context.brand_details_page = BrandDetailsPage(context.driver)
    for brand_link in context.company_brands_page.brand_links:
        context.driver.get(brand_link)
        details = context.brand_details_page.retrieve_details()
        ic(details)


@then(u'I should retrieve the required information for each brand')
def step_impl(context):
    pass