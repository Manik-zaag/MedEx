from behave import *
from icecream import ic

from pages.CompanyBrandsPage import CompanyBrandsPage
from pages.CompanyPage import CompanyPage


@given(u'I navigate to the MedEx Companies page')
def step_impl(context):
    context.company_page = CompanyPage(context.driver)
    context.company_page.navigate_to_base_page(context)
    assert context.company_page.display_status_of_company_page()


@when(u'I click on each company name')
def step_impl(context):
    # context.company_page.handle_pagination()
    # ic(len(context.company_page.company_links))
    # ic(context.company_page.company_links)
    pass


@when(u'I view all brands if available')
def step_impl(context):
    # for company_link in context.company_page.company_links:
    #     context.driver.get(company_link)
    #     context.company_brands_page = CompanyBrandsPage(context.driver)
    #     assert context.company_brands_page.retrieve_current_url().__eq__(company_link)
    context.company_brands_page = CompanyBrandsPage(context.driver)
    context.driver.get("https://medex.com.bd/companies/304/alien-pharma/brands")

    context.company_brands_page.handle_pagination()


@when(u'I click on each brand')
def step_impl(context):
    pass


@then(u'I should retrieve the required information for each brand')
def step_impl(context):
    pass