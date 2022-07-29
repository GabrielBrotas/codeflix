import { ListCategoriesUseCase } from '@gb/core/dist/application/category/use-cases';
import { SortDirection } from '@gb/core/dist/domain/@seedwork';

export class SearchCategoryDto implements ListCategoriesUseCase.Input {
  page?: number;
  per_page?: number;
  sort?: string;
  sort_dir?: SortDirection;
  filter?: string;
}
