import pytest

from pydantic import ValidationError
from pydantic_extra_types.color import Color 

from app.models.categories import CategoryCreate


def test_category_create():
  cc1 = CategoryCreate(name='Test category1', color=Color('black'))
  cc2 = CategoryCreate(name='Test category2', color='purple')

  assert cc1.color == '#000'
  assert cc2.color == '#800080'


def test_category_with_incorrect_color():
  with pytest.raises(ValidationError):
    CategoryCreate(name='Test category', color='asdf')

def test_category_with_incorrect_value():
  with pytest.raises(ValidationError):
    CategoryCreate(name='Test category', color=123)